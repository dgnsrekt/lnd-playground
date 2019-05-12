import luigi
import logme
import wget
import tarfile
from pathlib import Path

from paths import BIN_PATH, LND_ZIP_FILENAME, LND_URL, LND_PATH, LNCLI_PATH

log = logme.log(scope="module", name="downloader")


class DownloadTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(str(BIN_PATH / LND_ZIP_FILENAME))

    def run(self):
        log.info("Downloading LND.")
        wget.download(LND_URL, self.output().path)


class FileExtractionTask(luigi.Task):
    def requires(self):
        return DownloadTask()

    def output(self):
        paths = [LND_PATH, LNCLI_PATH]
        paths = [luigi.LocalTarget(str(path)) for path in paths]
        return paths

    def run(self):
        log.info("Extracting LND.")
        tar = tarfile.open(self.input().path)
        tar.extractall(BIN_PATH)
        tar.close()

        for p in self.output():
            print(Path(p.path).exists())


class DownloadExtractWrapper(luigi.WrapperTask):
    def requires(self):
        return FileExtractionTask()


def main():
    luigi.build([DownloadExtractWrapper()], local_scheduler=True)


if __name__ == "__main__":
    main()
