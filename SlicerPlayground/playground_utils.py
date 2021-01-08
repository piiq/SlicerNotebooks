"""
Utility fuctions for Slicer Playground.

These functions are copies from notebooks where they were created to enable reuse.
"""
import numpy as np
import vtk
import slicer
from emoji import UNICODE_EMOJI


def create_np_text_img(text: str, size: tuple = (128, 128),
                       font_size: int = 24, emoj_size: int = 64) -> np.ndarray:
    """
    Create a numpy text image.

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


def fit_slice_view(sliceView: str = 'all'):
    """
    Fit slice field of view to data.

    :param      sliceView:   Either one of default slice views ['Red', 'Green', 'Yellow'] or 'all'.
    :type       sliceView:   str
    """
    if sliceView == 'all':
        sliceView = slicer.app.layoutManager().sliceViewNames()
    elif sliceView in ['Red', 'Yellow', 'Green']:
        sliceView = [sliceView]
    for sv in sliceView:
        sliceViewWidget = slicer.app.layoutManager().sliceWidget(sv)
        sliceWidgetLogic = sliceViewWidget.sliceLogic()
        sliceWidgetLogic.FitSliceToAll()
    pass


def log_image_info(volume: slicer.vtkMRMLScalarVolumeNode):
    """Log basic image information to console."""
    print(f'Volume name: {volume.GetName()}')
    print(f'Origin: {volume.GetOrigin()}')
    print(f'Spacing: {volume.GetSpacing()}')
    print(f'Dimensions: {volume.GetImageData().GetDimensions()}\n')


def layout_3_volumes(volumeList: list):
    """Prepare 3x3 layout with 3 volumes in slice views."""
    ORIENTATIONS = ["Axial", "Sagittal", "Coronal"]
    THREE_BY_THREE_SLICES = [['Red', 'Yellow', 'Green'],
                             ['Slice4', 'Slice5', 'Slice6'],
                             ['Slice7', 'Slice8', 'Slice9']]
    for volumeIndex in range(3):
        inputVolumeNode = slicer.mrmlScene.GetFirstNodeByName(volumeList[volumeIndex])
        for view in THREE_BY_THREE_SLICES[volumeIndex]:
            show_slice_in_slice_view(volumeNode=inputVolumeNode,
                                     sliceView=view)
            sliceWidgetNode = slicer.app.layoutManager().sliceWidget(view).mrmlSliceNode()
            sliceWidgetNode.SetOrientation(ORIENTATIONS[THREE_BY_THREE_SLICES[volumeIndex].index(view)])


def create_seed_geometry(seedPositions: list, seedSize: int) -> vtk.vtkPolyData:
    """
    Create spheres at given positions.

    :param      seedPositions:  A list of lists of seed coordinates [r, a, s]
    :type       seedPositions:  list
    :param      seedSize:       The sphere diameter
    :type       seedSize:       int

    :returns:   A vtk filter that has vtkPolyData as output
    :rtype:     vtkPolyData
    """
    seedGeometry = vtk.vtkAppendPolyData()
    for position in seedPositions:
        seed = vtk.vtkSphereSource()
        seed.SetCenter(position)
        seed.SetRadius(seedSize)
        seed.Update()
        seedGeometry.AddInputData(seed.GetOutput())
        seedGeometry.Update()
    return seedGeometry


def rotate_x(geometry: vtk.vtkPolyData,
             angle: int,
             centerPoint: list) -> vtk.vtkTransformPolyDataFilter:
    """
    Rotate vtkPolyData axainst X axis.

    Generates a transform filter
    and applies rotation to a vtkPolyData input.

    :param      geometry:     The geometry
    :type       geometry:     vtkPolyData
    :param      angle:        The angle (degrees)
    :type       angle:        int
    :param      centerPoint:  Coordinates of the PolyData center
    :type       centerPoint:  list

    :returns:   A vtk filter that has the rotated data as output.
    :rtype:     vtkTransformPolyDataFilter
    """
    transform = vtk.vtkTransform()
    transform.Translate(centerPoint[0], centerPoint[1], centerPoint[2])
    transform.RotateX(angle)
    transform.Translate(-centerPoint[0], -centerPoint[1], -centerPoint[2])
    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetTransform(transform)
    transformFilter.SetInputConnection(geometry.GetOutputPort())
    transformFilter.Update()
    return transformFilter
