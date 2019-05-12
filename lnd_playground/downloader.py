import luigi
import logme
import wget
import tarfile
from pathlib import Path

from paths import ROOT_PATH, BIN_PATH, DOWNLOAD_URL, DOWNLOAD_FILE_PATH, EXTRACTED_FOLDER_PATH

log = logme.log(scope="module", name="downloader")


class DownloadFileTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(str(DOWNLOAD_FILE_PATH))

    def run(self):
        log.info("Downloading LND.")
        wget.download(DOWNLOAD_URL, self.output().path)


class ExtractFilesTask(luigi.Task):
    def requires(self):
        return DownloadFileTask()

    def output(self):
        return luigi.LocalTarget(str(EXTRACTED_FOLDER_PATH))

    def run(self):
        log.info("Extracting LND.")
        with tarfile.open(self.input().path) as tar:
            tar.extractall(ROOT_PATH)

        assert Path(self.output().path).exists()


class RenameFolderTask(luigi.Task):
    def requires(self):
        return ExtractFilesTask()

    def output(self):
        return luigi.LocalTarget(str(BIN_PATH))

    def run(self):
        Path(self.input().path).replace(BIN_PATH)


class DownloaderPipeline(luigi.WrapperTask):
    def requires(self):
        return RenameFolderTask()


def download_lightning_network_daemon_tools():
    return luigi.build([DownloaderPipeline()], local_scheduler=True)


def clean_up_lightning_network_daemon_tools():
    if EXTRACTED_FOLDER_PATH.exists():
        for file in EXTRACTED_FOLDER_PATH.glob("*"):
            file.unlink()
        EXTRACTED_FOLDER_PATH.rmdir()

    if DOWNLOAD_FILE_PATH.exists():
        DOWNLOAD_FILE_PATH.unlink()


#
clean_up_lightning_network_daemon_tools()
download_lightning_network_daemon_tools()
