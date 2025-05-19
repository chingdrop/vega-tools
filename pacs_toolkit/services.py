import numpy as np
import pandas as pd

from common.pandas_tools import audit_images
from config.django.enums import DICOM_2D_SERIES_DESCRIPTIONS, DICOM_3D_SERIES_DESCRIPTIONS


def audit_series_by_study_df(df: pd.DataFrame) -> pd.DataFrame:
    df.replace('<NONE>', np.nan, inplace=True)
    df.drop('File', axis=1, inplace=True)
    df.rename(
        columns={
            '0008:0050': 'Accession',
            '0010:0020': 'PID',
            '0008:0018': 'SOP Instance UID',
            '0008:0008': 'Image Type',
            '0028:0008': 'Number of Frames',
            '0020:0062': 'Image Laterality (2D Only)',
            '5200:9229.#0.0020:9071.#0.0020:9072': 'Frame Laterality (3D Only)',
            '5200:9229.#0.0028:9110.#0.0018:0050': 'Slice Thickness',
            '0054:0220.#0.0008:0100': 'View Code',
            '0054:0220.#0.0054:0222.#0.0008:0100': 'View Modifier Code',
            '0008:0070': 'Manufacturer',
            '0008:1090': 'Model',
            '0008:103E': 'Series Description',
            '0008:1030': 'Study Description',
            '0002:0010': 'Transfer Syntax'
        },
        inplace=True
    )
    df_2d = audit_images(df, '2D', DICOM_2D_SERIES_DESCRIPTIONS)
    df_3d = audit_images(df, '3D', DICOM_3D_SERIES_DESCRIPTIONS, slice_thickness=1)
    out = pd.concat([df_2d, df_3d])
    out.sort_values(['Accession'], inplace=True)
    return out
