import itertools
import logging
import pathlib
from typing import List

import face_recognition

from config import IMAGE_EXTENSIONS
from util import g_path, logger


def filter_dir(dir):
    yield from filter(lambda x: x.suffix in IMAGE_EXTENSIONS, g_path(dir).iterdir())


class FaceRec:
    def __init__(self, gakki_dir):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.known_faces = []
        for file_path in filter_dir(gakki_dir):  # type:pathlib.Path
            try:
                gakki_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file(file_path))
                self.logger.info("found:{:>3}, file_name:{}".format(len(gakki_face_encoding), file_path))
                self.known_faces.extend(gakki_face_encoding[0:min(1, len(gakki_face_encoding))])
            except Exception as e:
                self.logger.exception(e)
                continue

    def recon(self, path):
        """
        result compare result
        :param path:
        :return: is gakki: True, no face match: False, no face detected: 2
        """
        fail_flag = 2
        for unknown_face in face_recognition.face_encodings(face_recognition.load_image_file(path)):
            votes = face_recognition.compare_faces(self.known_faces, unknown_face, tolerance=0.45)  # type: List
            result = votes.count(True) > 0
            self.logger.info("{}:{}".format(votes, result))
            if result:
                return result
            else:
                fail_flag = False
        return fail_flag


def select_gakki():
    all_dir = "img"
    gakki_dir = "gakki_img"
    not_gakki_dir = "not_gakki_img"
    no_face_dir = "no_face_detected"
    fr = FaceRec("know")

    clock = itertools.count()
    for file_path in filter_dir(all_dir):  # type:pathlib.Path
        logging.info("recognizing {}: {}".format(next(clock), file_path))
        ok_path = g_path(gakki_dir, file_path.name)
        fail_path = g_path(not_gakki_dir, file_path.name)
        no_face_path = g_path(no_face_dir, file_path.name)
        if ok_path.exists() or fail_path.exists() or no_face_path.exists():
            # already compared continue
            continue
        try:
            result = fr.recon(file_path)
            if result is True:
                ok_path.symlink_to(file_path.absolute())
            elif result == 2:
                no_face_path.symlink_to(file_path.absolute())
            else:
                fail_path.symlink_to(file_path.absolute())
        except Exception as e:
            logger.exception(e)
            continue


if __name__ == "__main__":
    # FaceRec("know").recon("know/<strong>gakki<strong>853.jpeg")
    select_gakki()
