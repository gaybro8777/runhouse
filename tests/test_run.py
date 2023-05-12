import logging
import pickle
import unittest
from pprint import pprint

import runhouse as rh

FUNC_NAME = "my_test_func"
FUNC_RUN_NAME = "my_test_run"
CTX_MGR_RUN = "my_run_activity"

CLI_RUN_NAME = "my_cli_run"
S3_BUCKET = "runhouse-runs"


def setup():
    from runhouse.rns.api_utils.utils import create_s3_bucket

    create_s3_bucket(S3_BUCKET)


def summer(a: int, b: int):
    return a + b


def func_with_artifacts():
    cpu = rh.cluster("^rh-cpu").save()
    logging.info(f"Saved cluster {cpu.name} to RNS")
    loaded_cluster = rh.load(name="@/rh-cpu")
    logging.info(f"Loaded cluster {loaded_cluster.name} from RNS")
    return loaded_cluster.name


def slow_func(a, b):
    import time

    time.sleep(200)
    return a + b


def create_rh_func(fn, func_name=FUNC_NAME):
    # TODO [JL] make this a pytest fixture (along with the `cpu` cluster)
    return rh.function(fn, system="^rh-cpu", name=func_name).save()


# ------------------------- CLI RUN ------------ ----------------------


def test_create_cli_python_command_run():
    # Run python commands on the specified system. Save the run results to the .rh/logs/<run_name> folder of the system.
    cpu = rh.cluster("^rh-cpu").up_if_not()
    return_codes = cpu.run_python(
        [
            "import runhouse as rh",
            "import logging",
            "cpu = rh.cluster('^rh-cpu')",
            "logging.info(f'On the cluster {cpu.name}!')",
            "rh.cluster('^rh-cpu').save()",
        ],
        name_run=CLI_RUN_NAME,
    )

    assert return_codes[0][0] == 0


def test_create_cli_command_run():
    # Run CLI command on the specified system. Save the run results to the .rh/logs/<run_name> folder of the system.
    cpu = rh.cluster("^rh-cpu").up_if_not()
    return_codes = cpu.run(["python --version"], name_run=CLI_RUN_NAME)

    assert return_codes[0][1].strip() == "Python 3.10.6"


def test_load_cli_command_run_from_cluster():
    # Run only exists on the cluster (hasn't yet been saved to RNS).
    cpu = rh.cluster("^rh-cpu").up_if_not()
    cli_run = cpu.get_run(CLI_RUN_NAME)
    assert cli_run


def test_save_cli_run_on_cluster_to_rns():
    cpu = rh.cluster("^rh-cpu").up_if_not()
    cli_run = cpu.get_run(CLI_RUN_NAME)
    cli_run.save(name=CLI_RUN_NAME)

    loaded_run_from_rns = rh.Run.from_name(name=CLI_RUN_NAME)
    assert loaded_run_from_rns


def test_read_cli_command_stdout():
    # Read the stdout from the system the command was run
    cli_run = rh.Run.from_name(name=CLI_RUN_NAME)
    output = cli_run.stdout()
    assert output == "Python 3.10.6"


def test_cli_run_exists_on_system():
    cli_run = rh.Run.from_name(name=CLI_RUN_NAME)
    assert rh.exists(cli_run.name, resource_type=rh.Run.RESOURCE_TYPE)


def test_delete_cli_run_from_system():
    cpu = rh.cluster("^rh-cpu").up_if_not()
    cli_run = cpu.get_run(CLI_RUN_NAME)
    cli_run.delete_in_system()

    assert not cli_run.exists_in_system()


def test_delete_cli_run_from_rns():
    cli_run = rh.Run.from_name(CLI_RUN_NAME)
    cli_run.delete_configs()
    assert not rh.exists(name=cli_run.name, resource_type=rh.Run.RESOURCE_TYPE)


# ------------------------- FUNCTION RUN ----------------------------------


def test_create_run_on_cluster():
    """Intializes a Run, which will run async on the cluster.
    Returns the Run's key, which points to a specific folder on the cluster where the Run data lives.
    (in .rh/logs/<run_key>)"""
    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    fn_run_key = my_func(1, 2, name_run=FUNC_RUN_NAME)
    assert isinstance(fn_run_key, str)


def test_read_fn_stdout():
    """Reads the stdout for the Run."""
    cpu = rh.cluster("^rh-cpu").up_if_not()
    fn_run = cpu.get_run(FUNC_RUN_NAME)
    stdout = fn_run.stdout()
    pprint(stdout)
    assert stdout


def test_load_existing_run_from_cluster():
    """Load the Run created above directly from the cluster."""
    # Run only exists on the cluster (hasn't yet been saved to RNS).
    cpu = rh.cluster("^rh-cpu").up_if_not()
    func_run = cpu.get_run(FUNC_RUN_NAME)
    assert func_run.result() == 3


def test_get_fn_run_by_name():
    """Load the Run created above from the cluster."""
    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    run_output = my_func.get(run_str=FUNC_RUN_NAME)

    assert run_output == 3


def test_get_or_run_existing_fn_by_name():
    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    run_output = my_func.get_or_run(run_name=FUNC_RUN_NAME)

    assert run_output == 3


@unittest.skip("Not yet implemented.")
def test_create_run_with_artifacts():
    run_name = "run_with_artifacts"
    cpu = rh.cluster("^rh-cpu").up_if_not()
    my_func = create_rh_func(func_with_artifacts, func_name="func_with_artifacts")

    res = my_func(name_run=run_name)
    print(f"Res: {res}")

    func_run = cpu.get_run(run_name)

    assert func_run.downstream_artifacts
    assert func_run.upstream_artifacts


def test_get_or_run_new_fn_by_name():
    """Checks if run already exists with name, if not create a new one and return the results synchronously"""
    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    run_output = my_func.get_or_run(run_name="my_new_run", a=1, b=2)

    assert run_output == 3


def test_get_or_run_new_fn_async():
    """Checks if run already exists with name, if not create a new one and return the run key, function will
    run async on the cluster"""
    # Create new run, trigger the execution async and get a run key in return (since function will have
    # status of "RUNNING")
    my_func = create_rh_func(slow_func, func_name=FUNC_NAME)
    new_run_key = my_func.get_or_run(run_name="async_run", run_async=True, a=1, b=2)
    assert isinstance(new_run_key, str)


def test_delete_async_run_from_system():
    cpu = rh.cluster("^rh-cpu").up_if_not()
    async_run = cpu.get_run("async_run")
    async_run.delete_in_system()
    assert not async_run.exists_in_system()


def test_get_or_run_new_fn():
    # Create a new run, get results synchronously
    my_func = create_rh_func(func_with_artifacts, func_name=FUNC_NAME)
    res = my_func.get_or_run(run_name="sync_run")
    assert res == "rh-cpu"


def test_save_fn_run_to_rns():
    """Saves run config to RNS"""
    cpu = rh.cluster("^rh-cpu").up_if_not()
    func_run = cpu.get_run(FUNC_RUN_NAME)
    assert func_run

    func_run.save(name=FUNC_RUN_NAME)
    loaded_run = rh.Run.from_name(name=FUNC_RUN_NAME)
    assert rh.exists(loaded_run.name, resource_type=rh.Run.RESOURCE_TYPE)


def test_create_anon_run_on_cluster(request):
    """Create a new Run without giving it an explicit name"""
    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    fn_run_key = my_func(1, 2, name_run=True)

    print(f"Created a Run with name: {fn_run_key}")

    # Since this is an anom run save its auto-generated name to the cache for re-use in later tests
    request.config.cache.set("anon_run_name", fn_run_key)

    assert isinstance(fn_run_key, str)


def test_get_anon_fn_run_by_name_from_system(request):
    # Load a Run by its specific name (not necessarily the latest one)
    run_name = request.config.cache.get("anon_run_name", None)
    assert (
        run_name
    ), "No anon run name found, run the test `test_create_anom_run` to generate one"

    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    run_output = my_func.get(run_str=run_name)

    assert run_output == 3


# TODO [JL] convert to a pytest fixture
def test_load_anon_run_from_cluster(request):
    run_name = request.config.cache.get("anon_run_name", None)
    assert (
        run_name
    ), "No anon run name found, run the test `test_create_anon_run` to save the name of the Run to the cache."

    cpu = rh.cluster("^rh-cpu").up_if_not()
    func_run = cpu.get_run(FUNC_RUN_NAME)

    if func_run.status == rh.Run.COMPLETED_STATUS:
        assert func_run.result() == 3
    elif func_run.status == rh.Run.RUNNING_STATUS:
        assert func_run.stdout()
    else:
        assert False, "Run is in an unexpected state"


def test_latest_fn_run():
    my_func = create_rh_func(summer, func_name=FUNC_NAME)
    run_output = my_func.get(run_str="latest")

    assert run_output == 3


def test_copy_fn_run_from_cluster_to_local():
    my_run = rh.Run.from_name(name=FUNC_RUN_NAME)
    my_local_run = my_run.to("here")
    assert my_local_run.exists_in_system()


def test_copy_fn_run_from_system_to_s3():
    cpu = rh.cluster("^rh-cpu").up_if_not()
    my_run = cpu.get_run(FUNC_RUN_NAME)
    my_run_on_s3 = my_run.to("s3", path=f"/{S3_BUCKET}/my_test_run")

    assert my_run_on_s3.exists_in_system()

    my_run_on_s3.delete_in_system()
    assert not my_run_on_s3.exists_in_system()


def test_read_fn_run_inputs_and_outputs():
    my_run = rh.Run.from_name(name=FUNC_RUN_NAME)
    inputs = my_run.inputs()
    assert pickle.loads(inputs) == {"args": [1, 2], "kwargs": {}}

    output = my_run.result()
    assert output == 3


def test_read_fn_run_from_rns():
    # Read the stdout saved when running the function on the cluster
    my_run = rh.Run.from_name(name=FUNC_RUN_NAME)
    stdout = my_run.stdout()
    pprint(stdout)
    assert stdout


def test_delete_fn_run_from_rns():
    func_run = rh.Run.from_name(FUNC_RUN_NAME)
    func_run.delete_configs()
    assert not rh.exists(name=func_run.name, resource_type=rh.Run.RESOURCE_TYPE)


def test_slow_running_fn_run():
    run_name = "slow_func_run"
    my_func = create_rh_func(slow_func, func_name="slow_func")
    run_key = my_func(2, 2, name_run=run_name)
    print(f"Run key: {run_key}")

    cpu = rh.cluster("^rh-cpu").up_if_not()
    func_run = cpu.get_run(FUNC_RUN_NAME)
    assert func_run

    func_run.delete_in_system()
    assert not func_run.exists_in_system()


# ------------------------- CTX MANAGER RUN ----------------------------------


def test_create_local_ctx_manager_run():
    from runhouse.rh_config import rns_client

    with rh.run(name=CTX_MGR_RUN) as r:
        # Add all Runhouse objects loaded or saved in the context manager to the Run's artifact registry
        # (upstream + downstream artifacts)
        my_func = rh.Function.from_name(FUNC_NAME)
        my_func.save("my_new_func")

        my_func(1, 2, name_run="my_new_run")

        current_run = my_func.system.get_run("my_new_run")
        run_res = current_run.result()
        print(f"Run result: {run_res}")

        cluster = rh.load(name="@/rh-cpu")
        print(f"Cluster loaded: {cluster.name}")

    print(f"Saved Run with name: {r.name} to path: {r.path}")

    # Artifacts include the rns resolved name (ex: "/jlewitt1/rh-cpu")
    expected_downstream = [
        rns_client.resolve_rns_path(a) for a in r.downstream_artifacts
    ]
    expected_upstream = [rns_client.resolve_rns_path(a) for a in r.upstream_artifacts]

    assert r.downstream_artifacts == expected_downstream
    assert r.upstream_artifacts == expected_upstream


def test_load_named_ctx_manager_run():
    ctx_run = rh.Run.from_file(name=CTX_MGR_RUN)
    assert ctx_run.exists_in_system()


def test_read_stdout_from_ctx_manager_run():
    ctx_run = rh.Run.from_file(name=CTX_MGR_RUN)
    stdout = ctx_run.stdout()
    pprint(stdout)
    assert stdout


def test_save_ctx_run_to_rns():
    ctx_run = rh.Run.from_file(name=CTX_MGR_RUN)
    ctx_run.save()
    assert rh.exists(name=ctx_run.name, resource_type=rh.Run.RESOURCE_TYPE)


def test_delete_run_from_system():
    ctx_run = rh.Run.from_file(name=CTX_MGR_RUN)
    ctx_run.delete_in_system()
    assert not ctx_run.exists_in_system()


def test_delete_run_from_rns():
    ctx_run = rh.Run.from_name(CTX_MGR_RUN)
    ctx_run.delete_configs()
    assert not rh.exists(name=ctx_run.name, resource_type=rh.Run.RESOURCE_TYPE)


if __name__ == "__main__":
    setup()
    unittest.main()
