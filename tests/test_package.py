import unittest
from pathlib import Path

import runhouse as rh
from runhouse import rh_config


def setup():
    pass


def summer(a, b):
    return a + b


def test_from_string():
    p = rh.Package.from_string("reqs:~/runhouse")
    if (Path.home() / "runhouse").exists():
        assert isinstance(p.install_target, rh.Folder)
        assert p.install_target.path == str(Path.home() / "runhouse")
    else:
        assert p.install_target == "~/runhouse"


def test_share_package():
    import shutil

    # Create a local temp folder to install for the package
    tmp_path = Path.cwd().parent / "tmp_package"
    tmp_path.mkdir(parents=True, exist_ok=True)
    for i in range(3):
        output_file = Path(f"{tmp_path}/sample_file_{i}.txt")
        output_file.write_text(f"file{i}")

    p = rh.Package.from_string("local:./tmp_package")
    p.name = "package_to_share"  # shareable resource requires a name

    c = rh.cluster(name="@/rh-cpu")
    p.to(system=c)

    p.share(
        users=["josh@run.house", "donny@run.house"],
        access_type="write",
        notify_users=False,
    )

    shutil.rmtree(tmp_path)

    # Confirm the package's folder is now on the cluster
    status_codes = c.run(commands=["ls tmp_package"])
    assert "sample_file_0.txt" in status_codes[0][1]


def test_share_git_package():
    git_package = rh.GitPackage(
        name="shared_git_package",
        git_url="https://github.com/runhouse/runhouse.git",
        install_method="pip",
        revision="v0.0.1",
    ).save()

    git_package.share(
        users=["donny@run.house", "josh@run.house"],
        access_type="read",
        notify_users=False,
    )
    assert rh.rns_client.exists(name_or_path="shared_git_package")


def test_load_shared_git_package():
    git_package = rh.Package.from_name(name="@/shared_git_package")
    assert git_package.config_for_rns


def test_local_package_function():
    cluster = rh.cluster("^rh-cpu").up_if_not()
    function = rh.function(fn=summer).to(cluster, env=["./"])

    req = function.env.reqs[0]
    assert isinstance(req, rh.Package)
    assert isinstance(req.install_target, rh.Folder)
    assert req.install_target.system == cluster


def test_local_package_to_cluster():
    system = rh.cluster("^rh-cpu").up_if_not()
    package = rh.Package.from_string("./").to(system)

    assert isinstance(package.install_target, rh.Folder)
    assert package.install_target.system == system


def test_mount_local_package_to_cluster():
    system = rh.cluster("^rh-cpu").up_if_not()
    mount_path = "package_mount"
    package = rh.Package.from_string("./").to(system, path=mount_path, mount=True)

    assert isinstance(package.install_target, rh.Folder)
    assert package.install_target.system == system
    assert mount_path in system.run(["ls"])[0][1]


def test_package_file_system_to_cluster():
    import shutil

    from runhouse.rns.api_utils.utils import create_s3_bucket

    s3_bucket_path = "runhouse-folder"
    create_s3_bucket(s3_bucket_path)
    folder_name = "tmp_s3_package"

    # Create a local temp folder to install for the package
    tmp_path = Path(rh_config.rns_client.locate_working_dir()) / folder_name
    tmp_path.mkdir(parents=True, exist_ok=True)
    for i in range(3):
        output_file = Path(f"{tmp_path}/sample_file_{i}.txt")
        output_file.write_text(f"file{i}")

    pkg = rh.Package.from_string(f"local:./{folder_name}")
    s3_pkg = pkg.to(system="s3", path=f"/{s3_bucket_path}/package-tests")
    assert s3_pkg.install_target.system == "s3"
    assert s3_pkg.install_target.exists_in_system()

    cluster = rh.cluster(name="^rh-cpu").up_if_not()
    s3_pkg.to(system=cluster, mount=True, path=folder_name)

    shutil.rmtree(tmp_path)

    # Confirm the package's folder is now on the cluster
    status_codes = cluster.run(commands=[f"ls {folder_name}"])
    assert "sample_file_0.txt" in status_codes[0][1]


def test_torch_installs():
    cuda_v116_url = "--index-url https://download.pytorch.org/whl/cu116"
    cuda_v117_url = "--index-url https://download.pytorch.org/whl/cu117"
    cuda_v118_url = "--index-url https://download.pytorch.org/whl/cu118"

    extra_index_url = "--extra-index-url https://pypi.python.org/simple/"

    # Receive a torch install command and associated cuda version, confirm that `install_cmd_for_torch` appends
    # the correct --index-url for the matching cuda version
    install_commands = {
        (f"torch==1.13.1 {cuda_v116_url}", "11.6"): f"torch==1.13.1 {cuda_v116_url} {extra_index_url}",
        (f"torch {extra_index_url}", "11.7"): f"torch {extra_index_url} {cuda_v117_url}",
        ("matchatorch", "11.6"): f"matchatorch {cuda_v116_url} {extra_index_url}",
        ("torch>=1.13.0, <2.0.0", "11.8"): f"torch>=1.13.0, <2.0.0 {cuda_v118_url} {extra_index_url}",
        (f"torch {cuda_v116_url} torchaudio {extra_index_url}", "11.6"): f"torch {cuda_v116_url} {extra_index_url} "
                                                                         f"torchaudio {extra_index_url} "
                                                                         f"{cuda_v116_url}",
        ("torch torchpudding", "11.7"): f"torch {cuda_v117_url} {extra_index_url} torchpudding {cuda_v117_url} "
                                        f"{extra_index_url}",
        ("torch>=1.13.0", "11.6"): f"torch>=1.13.0 {cuda_v116_url} {extra_index_url}",
        ("torch>1.13.0", "11.6"): f"torch>1.13.0 {cuda_v116_url} {extra_index_url}",
        ("torch==1.13.0", "11.6"): f"torch==1.13.0 {cuda_v116_url} {extra_index_url}",
        ("torch~=1.13.0", "11.7"): f"torch~=1.13.0 {cuda_v117_url} {extra_index_url}",
        (f"torch==99.99.999 {cuda_v117_url}", "11.7"): f"torch==99.99.999 {cuda_v117_url} {extra_index_url}",
    }
    for (torch_version, cuda_version), expected_install_cmd in install_commands.items():
        dummy_pkg = rh.Package.from_string(specifier=f"pip:{torch_version}")
        formatted_install_cmd = dummy_pkg.install_cmd_for_torch(torch_version, cuda_version)

        assert (
                formatted_install_cmd == expected_install_cmd
        ), f"Unexpected result for {(torch_version, cuda_version)} "


if __name__ == "__main__":
    setup()
    unittest.main()
