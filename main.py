import os
import subprocess
from sys import platform as _platform

import projections
import cubes
import mountain
import kde
import christmas


def get_imagemagick_path(binary="convert"):
    if _platform == "linux" or _platform == "linux2":
        return os.path.join(os.path.sep, "usr", "bin", binary)
    elif _platform == "darwin":  # macOS (OS X)
        return os.path.join(os.path.sep, "opt", "local", "bin", binary)
    elif _platform == "win32":  # Windows
        return '"' + os.path.join('c:', os.path.sep, 'Program Files',
                                  'ImageMagick-7.0.8-Q16', binary+".exe") + '"'


def convert_images_format(ims_folder, format_from="svg", format_to="png",
                          resolution="500x500", create_new_ims=True,
                          quality="100"):
    print("Converting %ss to %ss..." % (format_from.upper(),
                                        format_to.upper()))
    subprocess.call(
        "{path_to_mogrify} -format {format_to} "
        "-quality {quality} {resizing} *.{format_from}".format(
            path_to_mogrify=get_imagemagick_path(binary="mogrify"),
            format_to=format_to, quality=quality,
            resizing="" if resolution is None else "-{option} {res}".format(
                option="size" if create_new_ims else "resize", res=resolution),
            format_from=format_from), shell=True, cwd=ims_folder)


def create_gif(ims_input_folder, gif_output_name, delay=2, ext="png"):
    # Create GIF with ImageMagick
    print("Stitching together a GIF from the frames of directory: %s..." % ims_input_folder)
    subprocess.call(
        "{path_to_convert} -delay {delay} "
        "{ims_folder}/*{ext} {gif_name}".format(
            path_to_convert=get_imagemagick_path(), delay=delay, ext=ext,
            ims_folder=ims_input_folder, gif_name=gif_output_name), shell=True)


if __name__ == '__main__':
    frames_folder = projections.create_animation_frames()
    create_gif(ims_input_folder=frames_folder,
               gif_output_name='projections.gif', delay=3)

    frames_folder = cubes.create_animation_frames()
    create_gif(ims_input_folder=frames_folder,
               gif_output_name='cubes.gif', delay=3)

    frames_folder = mountain.create_animation_frames()
    create_gif(ims_input_folder=frames_folder,
               gif_output_name='mountain.gif', delay=4)

    frames_folder = kde.create_animation_frames()
    convert_images_format(frames_folder, format_from="png", format_to="png",
                          resolution="500x500", create_new_ims=False)
    create_gif(ims_input_folder=frames_folder,
               gif_output_name='kde.gif', delay=4)

    frames_folder = christmas.create_animation_frames()
    create_gif(ims_input_folder=frames_folder,
               gif_output_name='christmas.gif', delay=2)
