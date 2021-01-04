"""
Utility fuctions for Slicer Playground.
These functions are copies from notebooks where they were created to enable reuse.
"""
import numpy as np
import slicer
from emoji import UNICODE_EMOJI


def create_np_text_img(text: str, size: tuple = (128, 128),
                       font_size: int = 24, emoj_size: int = 64) -> np.ndarray:
    """
    Creates a numpy text image.

    Creates a text-on-background image and returns it as a flat 3D numpy array.
    
    Check font paths when copying this function.
    The font paths should point to actual true-type font files on the disk.

    :param      text:  Input unicode text.
    :type       text:  str
    :param      size:  Target image size (optional).
    :type       size:  tuple
    :param      font_size:  Font size of the text (optional).
    :type       font_size:  int

    :returns:   Flat 3D numpy array containing pixel values.
    :rtype:     np.ndarray
    """
    from PIL import Image, ImageDraw, ImageFont
    if bool(set(text).intersection(UNICODE_EMOJI)):
        font_path = "/System/Library/Fonts/Apple Color Emoji.ttc"
        font = ImageFont.truetype(font_path, emoj_size)
    else:
        font_path = "/System/Library/Fonts/Microsoft/Arial Black.ttf"
        font = ImageFont.truetype(font_path, font_size)

    text_width, text_height = font.getsize(text)

    text_image = Image.new('I', size, "black")
    draw = ImageDraw.Draw(text_image)
    draw.text((text_width/2, text_height/2), text, 'white', font)
    return np.asarray(text_image).reshape(*size, 1)

def show_slice_in_slice_view(volumeNode: slicer.vtkMRMLScalarVolumeNode,
                             sliceNum: int = 0,
                             sliceView: str = 'Red'):
    """
    Render a numpy image on slice view.

    :param      volumeNode:  The volume node
    :type       volumeNode:  vtkMRMLScalarVolumeNode
    :param      sliceNum:    The number of the slice that we want to show. Optional. Defaults to 0.
    :type       sliceNum:    int
    :param      sliceView:   One of default slice views ('Red', 'Green', 'Yellow')
    :type       sliceView:   str
    """
    sliceViewWidget = slicer.app.layoutManager().sliceWidget(sliceView)
    sliceWidgetLogic = sliceViewWidget.sliceLogic()
    sliceWidgetLogic.GetSliceCompositeNode().SetBackgroundVolumeID(volumeNode.GetID())
    sliceWidgetLogic.FitSliceToAll()
    sliceWidgetLogic.SetSliceOffset(sliceNum)
    pass

