# Copyright (c) 2021 CNES
#
# All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
import pickle
import pytest
import math
import numpy as np
from pyinterp import core
from pyinterp.core import geodetic

POINTS = [(-36.25, -54.9238), (-36.5, -54.9238), (-36.75, -54.9238),
          (-37, -54.9238), (-37.25, -54.9238), (-37.5, -54.9238),
          (-37.75, -54.9238), (-38, -54.9238), (-38.25, -54.9238),
          (-38.5, -54.9238), (-38.75, -54.9238), (-39, -54.9238),
          (-39.25, -54.9238), (-39.5, -54.9238), (-39.75, -54.9238),
          (-40, -54.9238), (-40.25, -54.9238), (-40.5, -54.9238),
          (-40.75, -54.9238), (-41, -54.9238), (-41.25, -54.9238),
          (-41.5, -54.9238), (-41.75, -54.9238), (-42, -54.9238),
          (-42.25, -54.9238), (-42.5, -54.9238), (-42.75, -54.9238),
          (-43, -54.9238), (-43.25, -54.9238), (-43.5, -54.9238),
          (-43.75, -54.9238), (-44, -54.9238), (-44.25, -54.9238),
          (-44.5, -54.9238), (-44.75, -54.9238), (-45, -54.9238),
          (-45.25, -54.9238), (-45.5, -54.9238), (-45.75, -54.9238),
          (-46, -54.9238), (-46.25, -54.9238), (-46.5, -54.9238),
          (-46.75, -54.9238), (-47, -54.9238), (-47.25, -54.9238),
          (-47.5, -54.9238), (-47.75, -54.9238), (-48, -54.9238),
          (-48.25, -54.9238), (-48.5, -54.9238), (-48.75, -54.9238),
          (-49, -54.9238), (-49.25, -54.9238), (-49.5, -54.9238),
          (-49.75, -54.9238), (-50, -54.9238), (-50.25, -54.9238),
          (-50.5, -54.9238), (-50.75, -54.9238), (-51, -54.9238),
          (-51.25, -54.9238), (-51.5, -54.9238), (-51.75, -54.9238),
          (-52, -54.9238), (-52.25, -54.9238), (-52.5, -54.9238),
          (-52.75, -54.9238), (-53, -54.9238), (-53.25, -54.9238),
          (-53.5, -54.9238), (-53.75, -54.9238), (-54, -54.9238),
          (-54.25, -54.9238), (-54.5, -54.9238), (-54.75, -54.9238),
          (-55, -54.9238), (-55.25, -54.9238), (-55.5, -54.9238),
          (-55.75, -54.9238), (-56, -54.9238), (-56.25, -54.9238),
          (-56.5, -54.9238), (-56.75, -54.9238), (-57, -54.9238),
          (-57.25, -54.9238), (-57.5, -54.9238), (-57.75, -54.9238),
          (-58, -54.9238), (-58.25, -54.9238), (-58.5, -54.9238),
          (-58.75, -54.9238), (-59, -54.9238), (-59.25, -54.9238),
          (-59.5, -54.9238), (-59.75, -54.9238), (-60, -54.9238),
          (-60.25, -54.9238), (-60.5, -54.9238), (-60.75, -54.9238),
          (-61, -54.9238), (-61.25, -54.9238), (-61.5, -54.9238),
          (-61.75, -54.9238), (-62, -54.9238), (-62.25, -54.9238),
          (-62.5, -54.9238), (-62.75, -54.9238), (-63, -54.9238),
          (-63.25, -54.9238), (-63.5, -54.9238), (-63.75, -54.9238),
          (-64, -54.9238), (-64.25, -54.9238), (-64.5, -54.9238),
          (-64.75, -54.9238), (-65, -54.9238), (-65.25, -54.9238),
          (-65.5, -54.9238), (-66.25, -54.4905), (-66.5, -54.345),
          (-67.25, -54.0525), (-67.5, -53.9055), (-67.75, -53.7579),
          (-68, -53.4613), (-69.25, -52.5588), (-69.25, -52.4066),
          (-69.25, -52.2538), (-69, -51.1695), (-69, -51.0125), (-69, -50.855),
          (-69, -50.6969), (-69, -50.5383), (-68.75, -50.3791),
          (-67.5, -49.0865), (-67.5, -46.3975), (-67.5, -46.2248),
          (-67.5, -46.0515), (-67.25, -45.7035), (-67, -45.3532),
          (-66.25, -45.0007), (-65.25, -43.7499), (-65, -42.1026),
          (-65, -41.9168), (-65, -41.7305), (-65, -41.5437), (-65, -41.3563),
          (-65, -41.1684), (-65, -40.9799), (-64.75, -40.9799),
          (-62.25, -39.0656), (-62, -39.0656), (-61.75, -39.0656),
          (-61.5, -39.0656), (-61.25, -39.0656), (-61, -39.0656),
          (-60, -38.8713), (-59.75, -38.8713), (-58.25, -34.4619),
          (-58.25, -34.2555), (-58, -34.2555), (-57, -34.6678),
          (-55.75, -34.8731), (-55.5, -34.8731), (-53.5, -34.0486),
          (-53.25, -33.8412), (-53, -33.6333), (-52.5, -33.0066),
          (-52.25, -32.3754), (-52, -32.164), (-51.75, -31.9522),
          (-51.5, -31.7398), (-51, -31.3136), (-50.25, -30.4554),
          (-50, -29.8068), (-49.5, -29.1539), (-49.25, -28.9353),
          (-48.5, -27.1704), (-48.5, -26.9478), (-48.5, -26.7247),
          (-48.5, -26.5012), (-48.5, -26.2772), (-48.5, -26.0528),
          (-48.5, -25.828), (-48.25, -25.3771), (-47.75, -24.9245),
          (-47, -24.4703), (-46.75, -24.2425), (-46, -23.7858),
          (-44.5, -23.0977), (-44.25, -23.0977), (-44, -23.0977),
          (-43.75, -23.0977), (-43.5, -23.0977), (-41.75, -22.4061),
          (-41, -21.4785), (-40.75, -21.0125), (-40.25, -20.3107),
          (-40, -19.8411), (-39.5, -18.424),
          (-39.5, -18.1867), (-39, -16.7559), (-39, -16.5164), (-39, -15.0731),
          (-39, -14.8315), (-39, -14.5897), (-39, -14.3477), (-39, -14.1053),
          (-38.75, -13.1335), (-37.5, -11.9132), (-37.25, -11.4236),
          (-37, -10.933), (-35.75, -9.70328), (-35, -8.71619),
          (-34.75, -7.72648), (-34.75, -7.47867), (-36.75, -4.99367),
          (-37.25, -4.74457), (-38, -4.24611), (-38.25, -3.99675),
          (-39.25, -3.24826), (-39.75, -2.99863), (-40.75, -2.74894),
          (-41, -2.74894), (-41.25, -2.74894), (-41.5, -2.74894),
          (-41.75, -2.74894), (-42, -2.74894), (-44.25, -2.74894),
          (-44.5, -2.74894), (-46.5, -0.999949), (-48.25, -0.999949),
          (-48.5, -0.999949), (-48.5, -0.749979), (-48.5, -0.499994),
          (-48.5, -0.249999), (-48.25, -0.249999), (-48, -0.249999),
          (-47.75, -0.249999), (-47.5, -0.249999), (-47.25, -0.249999),
          (-47, -0.249999), (-46.75, -0.249999), (-46.5, -0.249999),
          (-46.25, -0.249999), (-46, -0.249999), (-45.75, -0.249999),
          (-45.5, -0.249999), (-45.25, -0.249999), (-45, -0.249999),
          (-44.75, -0.249999), (-44.5, -0.249999), (-44.25, -0.249999),
          (-44, -0.249999), (-43.75, -0.249999), (-43.5, -0.249999),
          (-43.25, -0.249999), (-43, -0.249999), (-42.75, -0.249999),
          (-42.5, -0.249999), (-42.25, -0.249999), (-42, -0.249999),
          (-41.75, -0.249999), (-41.5, -0.249999), (-41.25, -0.249999),
          (-41, -0.249999), (-40.75, -0.249999), (-40.5, -0.249999),
          (-40.25, -0.249999), (-40, -0.249999), (-39.75, -0.249999),
          (-39.5, -0.249999), (-39.25, -0.249999), (-39, -0.249999),
          (-38.75, -0.249999), (-38.5, -0.249999), (-38.25, -0.249999),
          (-38, -0.249999), (-37.75, -0.249999), (-37.5, -0.249999),
          (-37.25, -0.249999), (-37, -0.249999), (-36.75, -0.249999),
          (-36.5, -0.249999), (-36.25, -0.249999), (-36, -0.249999),
          (-35.75, -0.249999), (-35.5, -0.249999), (-35.25, -0.249999),
          (-35, -0.249999), (-34.75, -0.249999), (-34.5, -0.249999),
          (-34.25, -0.249999), (-34, -0.249999), (-33.75, -0.249999),
          (-33.5, -0.249999), (-33.25, -0.249999), (-33, -0.249999),
          (-32.75, -0.249999), (-32.5, -0.249999), (-32.25, -0.249999),
          (-32, -0.249999), (-31.75, -0.249999), (-31.5, -0.249999),
          (-31.25, -0.249999), (-31, -0.249999), (-30.75, -0.249999),
          (-30.5, -0.249999), (-30.25, -0.249999), (-30, -0.249999),
          (-29.75, -0.249999), (-29.5, -0.249999), (-29.25, -0.249999),
          (-29, -0.249999), (-28.75, -0.249999), (-28.5, -0.249999),
          (-28.25, -0.249999), (-28, -0.249999), (-27.75, -0.249999),
          (-27.5, -0.249999), (-27.25, -0.249999), (-27, -0.249999),
          (-26.75, -0.249999), (-26.5, -0.249999), (-26.25, -0.249999),
          (-26, -0.249999), (-25.75, -0.249999), (-25.5, -0.249999),
          (-25.25, -0.249999), (-25, -0.249999), (-24.75, -0.249999),
          (-24.5, -0.249999), (-24.25, -0.249999), (-24, -0.249999),
          (-23.75, -0.249999), (-23.5, -0.249999), (-23.25, -0.249999),
          (-23, -0.249999), (-22.75, -0.249999), (-22.5, -0.249999),
          (-22.25, -0.249999), (-22, -0.249999), (-21.75, -0.249999),
          (-21.5, -0.249999), (-21.25, -0.249999), (-21, -0.249999),
          (-20.75, -0.249999), (-20.5, -0.249999), (-20.25, -0.249999),
          (-20, -0.249999), (-19.75, -0.249999), (-19.5, -0.249999),
          (-19.25, -0.249999), (-19, -0.249999), (-18.75, -0.249999),
          (-18.5, -0.249999), (-18.25, -0.249999), (-18, -0.249999),
          (-17.75, -0.249999), (-17.5, -0.249999), (-17.25, -0.249999),
          (-17, -0.249999), (-16.75, -0.249999), (-16.5, -0.249999),
          (-16.25, -0.249999), (-16, -0.249999), (-15.75, -0.249999),
          (-15.5, -0.249999), (-15.25, -0.249999), (-15, -0.249999),
          (-14.75, -0.249999), (-14.5, -0.249999), (-14.25, -0.249999),
          (-14, -0.249999), (-13.75, -0.249999), (-13.5, -0.249999),
          (-13.25, -0.249999), (-13, -0.249999), (-12.75, -0.249999),
          (-12.5, -0.249999), (-12.25, -0.249999), (-12, -0.249999),
          (-11.75, -0.249999), (-11.5, -0.249999), (-11.25, -0.249999),
          (-11, -0.249999), (-10.75, -0.249999), (-10.5, -0.249999),
          (-10.25, -0.249999), (-10, -0.249999), (-9.75, -0.249999),
          (-9.5, -0.249999), (-9.25, -0.249999), (-9, -0.249999),
          (-8.75, -0.249999), (-8.5, -0.249999), (-8.25, -0.249999),
          (-8, -0.249999), (-7.75, -0.249999), (-7.5, -0.249999),
          (-7.25, -0.249999), (-7, -0.249999), (-6.75, -0.249999),
          (-6.5, -0.249999), (-6.25, -0.249999), (-6, -0.249999),
          (-5.75, -0.249999), (-5.5, -0.249999), (-5.25, -0.249999),
          (-5, -0.249999), (-4.75, -0.249999), (-4.5, -0.249999),
          (-4.25, -0.249999), (-4, -0.249999), (-3.75, -0.249999),
          (-3.5, -0.249999), (-3.25, -0.249999), (-3, -0.249999),
          (-2.75, -0.249999), (-2.5, -0.249999), (-2.25, -0.249999),
          (-2, -0.249999), (-1.75, -0.249999), (-1.5, -0.249999),
          (-1.25, -0.249999), (-1, -0.249999), (-0.75, -0.249999),
          (-0.5, -0.249999), (-0.25, -0.249999), (-1.81899e-12, -0.249999),
          (0.25, -0.249999), (0.5, -0.249999), (0.75, -0.249999), (1,
                                                                   -0.249999),
          (1.25, -0.249999), (1.5, -0.249999), (1.75, -0.249999), (2,
                                                                   -0.249999),
          (2.25, -0.249999), (2.5, -0.249999), (2.75, -0.249999), (3,
                                                                   -0.249999),
          (3.25, -0.249999), (3.5, -0.249999), (3.75, -0.249999), (4,
                                                                   -0.249999),
          (4.25, -0.249999), (4.5, -0.249999), (4.75, -0.249999), (5,
                                                                   -0.249999),
          (5.25, -0.249999), (5.5, -0.249999), (5.75, -0.249999), (6,
                                                                   -0.249999),
          (6.25, -0.249999), (6.5, -0.249999), (6.75, -0.249999), (7,
                                                                   -0.249999),
          (7.25, -0.249999), (7.5, -0.249999), (7.75, -0.249999), (8,
                                                                   -0.249999),
          (8.25, -0.249999), (8.5, -0.249999), (8.75, -0.249999), (9,
                                                                   -0.249999),
          (9.25, -0.249999), (9.75, -2.49921), (10.25, -2.99863),
          (10.75, -3.49783), (11.25, -3.99675), (11.75, -4.74457),
          (12, -5.24267), (12.25, -5.98906), (12.75, -6.98265), (13, -7.72648),
          (13.25, -8.22164), (13.25, -8.46899), (13.25, -8.71619),
          (13.5, -10.4417), (13.75, -10.933), (13.75, -11.1784),
          (13.75, -11.4236), (13.75, -11.6685), (13.75, -11.9132),
          (13.5, -12.402), (12.5, -13.6199), (12.25, -14.5897), (12, -15.5553),
          (11.75, -16.7559), (12.5, -19.1341), (12.75, -19.6058),
          (13, -20.0761), (13.25, -20.545), (13.5, -21.0125),
          (13.75, -21.4785), (14.25, -22.1747), (14.5, -22.637),
          (14.5, -22.8675), (14.5, -24.2425), (14.75, -24.9245),
          (14.75, -25.151), (14.75, -25.3771), (15, -26.5012), (16, -28.2769),
          (16.5, -28.7163), (16.75, -29.1539),
          (17, -29.8068), (17.25, -30.4554), (17.5, -30.8855), (18, -31.5269),
          (18.25, -31.9522), (18.25, -32.164), (18.25, -32.3754),
          (19.25, -34.4619), (19.75, -34.8731), (19.75, -35.078),
          (19.75, -35.2823), (19.75, -35.4861), (19.75, -35.6894),
          (19.75, -35.8922), (19.75, -36.0945), (19.75, -36.2962),
          (19.75, -36.4975), (19.75, -36.6982), (19.75, -36.8984),
          (19.75, -37.098), (19.75, -37.2972), (19.75, -37.4958),
          (19.75, -37.6939), (19.75, -37.8914), (19.75, -38.0885),
          (19.75, -38.285), (19.75, -38.4809), (19.75, -38.6764),
          (19.75, -38.8713), (19.75, -39.0656), (19.75, -39.2595),
          (19.75, -39.4528), (19.75, -39.6456), (19.75, -39.8378),
          (19.75, -40.0295), (19.75, -40.2206), (19.75, -40.4113),
          (19.75, -40.6013), (19.75, -40.7909), (19.75, -40.9799),
          (19.75, -41.1684), (19.75, -41.3563), (19.75, -41.5437),
          (19.75, -41.7305), (19.75, -41.9168), (19.75, -42.1026),
          (19.75, -42.2878), (19.75, -42.4725), (19.75, -42.6566),
          (19.75, -42.8402), (19.75, -43.0232), (19.75, -43.2057),
          (19.75, -43.3877), (19.75, -43.5691), (19.75, -43.7499),
          (19.75, -43.9303), (19.75, -44.11), (19.75, -44.2893),
          (19.75, -44.4679), (19.75, -44.6461), (19.75, -44.8237),
          (19.75, -45.0007), (19.75, -45.1772), (19.75, -45.3532),
          (19.75, -45.5286), (19.75, -45.7035), (19.75, -45.8778),
          (19.75, -46.0515), (19.75, -46.2248), (19.75, -46.3975),
          (19.75, -46.5696), (19.75, -46.7412), (19.75, -46.9123),
          (19.75, -47.0828), (19.75, -47.2527), (19.75, -47.4221),
          (19.75, -47.591), (19.75, -47.7593), (19.75, -47.9271),
          (19.75, -48.0944), (19.75, -48.2611), (19.75, -48.4273),
          (19.75, -48.5929), (19.75, -48.758), (19.75, -48.9225),
          (19.75, -49.0865), (19.75, -49.25), (19.75, -49.4129),
          (19.75, -49.5753), (19.75, -49.7371), (19.75, -49.8984),
          (19.75, -50.0592), (19.75, -50.2194), (19.75, -50.3791),
          (19.75, -50.5383), (19.75, -50.6969), (19.75, -50.855),
          (19.75, -51.0125), (19.75, -51.1695), (19.75, -51.326),
          (19.75, -51.482), (19.75, -51.6374), (19.75, -51.7923),
          (19.75, -51.9467), (19.75, -52.1005), (19.75, -52.2538),
          (19.75, -52.4066), (19.75, -52.5588), (19.75, -52.7106),
          (19.75, -52.8618), (19.75, -53.0124), (19.75, -53.1626),
          (19.75, -53.3122), (19.75, -53.4613), (19.75, -53.6099),
          (19.75, -53.7579), (19.75, -53.9055), (19.75, -54.0525),
          (19.75, -54.199), (19.75, -54.345), (19.75, -54.4905),
          (19.75, -54.6354), (19.75, -54.7799), (19.75,
                                                 -54.9238), (19.5, -54.9238),
          (19.25, -54.9238), (19, -54.9238), (18.75, -54.9238), (18.5,
                                                                 -54.9238),
          (18.25, -54.9238), (18, -54.9238), (17.75, -54.9238), (17.5,
                                                                 -54.9238),
          (17.25, -54.9238), (17, -54.9238), (16.75, -54.9238), (16.5,
                                                                 -54.9238),
          (16.25, -54.9238), (16, -54.9238), (15.75, -54.9238), (15.5,
                                                                 -54.9238),
          (15.25, -54.9238), (15, -54.9238), (14.75, -54.9238), (14.5,
                                                                 -54.9238),
          (14.25, -54.9238), (14, -54.9238), (13.75, -54.9238), (13.5,
                                                                 -54.9238),
          (13.25, -54.9238), (13, -54.9238), (12.75, -54.9238), (12.5,
                                                                 -54.9238),
          (12.25, -54.9238), (12, -54.9238), (11.75, -54.9238), (11.5,
                                                                 -54.9238),
          (11.25, -54.9238), (11, -54.9238), (10.75, -54.9238), (10.5,
                                                                 -54.9238),
          (10.25, -54.9238), (10, -54.9238), (9.75, -54.9238), (9.5, -54.9238),
          (9.25, -54.9238), (9, -54.9238), (8.75, -54.9238), (8.5, -54.9238),
          (8.25, -54.9238), (8, -54.9238), (7.75, -54.9238), (7.5, -54.9238),
          (7.25, -54.9238), (7, -54.9238), (6.75, -54.9238), (6.5, -54.9238),
          (6.25, -54.9238), (6, -54.9238), (5.75, -54.9238), (5.5, -54.9238),
          (5.25, -54.9238), (5, -54.9238), (4.75, -54.9238), (4.5, -54.9238),
          (4.25, -54.9238), (4, -54.9238), (3.75, -54.9238), (3.5, -54.9238),
          (3.25, -54.9238), (3, -54.9238), (2.75, -54.9238), (2.5, -54.9238),
          (2.25, -54.9238), (2, -54.9238), (1.75, -54.9238), (1.5, -54.9238),
          (1.25, -54.9238), (1, -54.9238), (0.75, -54.9238), (0.5, -54.9238),
          (0.25, -54.9238), (-1.81899e-12, -54.9238), (-0.25, -54.9238),
          (-0.5, -54.9238), (-0.75, -54.9238), (-1, -54.9238), (-1.25,
                                                                -54.9238),
          (-1.5, -54.9238), (-1.75, -54.9238), (-2, -54.9238), (-2.25,
                                                                -54.9238),
          (-2.5, -54.9238), (-2.75, -54.9238), (-3, -54.9238), (-3.25,
                                                                -54.9238),
          (-3.5, -54.9238), (-3.75, -54.9238), (-4, -54.9238), (-4.25,
                                                                -54.9238),
          (-4.5, -54.9238), (-4.75, -54.9238), (-5, -54.9238), (-5.25,
                                                                -54.9238),
          (-5.5, -54.9238), (-5.75, -54.9238), (-6, -54.9238), (-6.25,
                                                                -54.9238),
          (-6.5, -54.9238), (-6.75, -54.9238), (-7, -54.9238), (-7.25,
                                                                -54.9238),
          (-7.5, -54.9238), (-7.75, -54.9238), (-8, -54.9238), (-8.25,
                                                                -54.9238),
          (-8.5, -54.9238), (-8.75, -54.9238), (-9, -54.9238), (-9.25,
                                                                -54.9238),
          (-9.5, -54.9238), (-9.75, -54.9238), (-10, -54.9238),
          (-10.25, -54.9238), (-10.5, -54.9238), (-10.75, -54.9238),
          (-11, -54.9238), (-11.25, -54.9238), (-11.5, -54.9238),
          (-11.75, -54.9238), (-12, -54.9238), (-12.25, -54.9238),
          (-12.5, -54.9238), (-12.75, -54.9238), (-13, -54.9238),
          (-13.25, -54.9238), (-13.5, -54.9238), (-13.75, -54.9238),
          (-14, -54.9238), (-14.25, -54.9238), (-14.5, -54.9238),
          (-14.75, -54.9238), (-15, -54.9238), (-15.25, -54.9238),
          (-15.5, -54.9238), (-15.75, -54.9238), (-16, -54.9238),
          (-16.25, -54.9238), (-16.5, -54.9238), (-16.75, -54.9238),
          (-17, -54.9238), (-17.25, -54.9238), (-17.5, -54.9238),
          (-17.75, -54.9238), (-18, -54.9238), (-18.25, -54.9238),
          (-18.5, -54.9238), (-18.75, -54.9238), (-19, -54.9238),
          (-19.25, -54.9238), (-19.5, -54.9238), (-19.75, -54.9238),
          (-20, -54.9238), (-20.25, -54.9238), (-20.5, -54.9238),
          (-20.75, -54.9238), (-21, -54.9238), (-21.25, -54.9238),
          (-21.5, -54.9238), (-21.75, -54.9238), (-22, -54.9238),
          (-22.25, -54.9238), (-22.5, -54.9238), (-22.75, -54.9238),
          (-23, -54.9238), (-23.25, -54.9238), (-23.5, -54.9238),
          (-23.75, -54.9238), (-24, -54.9238), (-24.25, -54.9238),
          (-24.5, -54.9238), (-24.75, -54.9238), (-25, -54.9238),
          (-25.25, -54.9238), (-25.5, -54.9238), (-25.75, -54.9238),
          (-26, -54.9238), (-26.25, -54.9238), (-26.5, -54.9238),
          (-26.75, -54.9238), (-27, -54.9238), (-27.25, -54.9238),
          (-27.5, -54.9238), (-27.75, -54.9238), (-28, -54.9238),
          (-28.25, -54.9238), (-28.5, -54.9238), (-28.75, -54.9238),
          (-29, -54.9238), (-29.25, -54.9238), (-29.5, -54.9238),
          (-29.75, -54.9238), (-30, -54.9238), (-30.25, -54.9238),
          (-30.5, -54.9238), (-30.75, -54.9238), (-31, -54.9238),
          (-31.25, -54.9238), (-31.5, -54.9238), (-31.75, -54.9238),
          (-32, -54.9238), (-32.25, -54.9238), (-32.5, -54.9238),
          (-32.75, -54.9238), (-33, -54.9238), (-33.25, -54.9238),
          (-33.5, -54.9238), (-33.75, -54.9238), (-34, -54.9238),
          (-34.25, -54.9238), (-34.5, -54.9238), (-34.75, -54.9238),
          (-35, -54.9238), (-35.25, -54.9238), (-35.5, -54.9238),
          (-35.75, -54.9238), (-36, -54.9238), (-36.25, -54.9238)]


def test_system_wgs84():
    """Checking expected WGS-84 properties"""
    wgs84 = core.geodetic.System()
    # https://fr.wikipedia.org/wiki/WGS_84
    # https://en.wikipedia.org/wiki/Geodetic_datum
    # http://earth-info.nga.mil/GandG/publications/tr8350.2/wgs84fin.pdf
    assert 6378137 == pytest.approx(wgs84.semi_major_axis)
    assert 1 / 298.257223563 == pytest.approx(wgs84.flattening)
    assert 6356752.314245179497563967 == pytest.approx(wgs84.semi_minor_axis())
    assert 0.081819190842622 == pytest.approx(math.sqrt(
        wgs84.first_eccentricity_squared()),
                                              abs=1e-15)
    assert 8.2094437949696 * 1e-2 == pytest.approx(math.sqrt(
        wgs84.second_eccentricity_squared()),
                                                   abs=1e-15)
    assert 40075.017 == pytest.approx(wgs84.equatorial_circumference() * 1e-3,
                                      abs=1e-3)
    assert 39940.652 == pytest.approx(wgs84.equatorial_circumference(False) *
                                      1e-3,
                                      abs=1e-3)
    assert 6399593.6258 == pytest.approx(wgs84.polar_radius_of_curvature(),
                                         abs=1e-4)
    assert 6335439.3272 == pytest.approx(
        wgs84.equatorial_radius_of_curvature(), abs=1e-4)
    assert 0.996647189335 == pytest.approx(wgs84.axis_ratio(), abs=1e-12)
    assert 5.2185400842339 * 1E5 == pytest.approx(wgs84.linear_eccentricity(),
                                                  abs=1e-6)
    assert 6371008.7714 == pytest.approx(wgs84.mean_radius(), abs=1e-4)
    assert 6371007.1809 == pytest.approx(wgs84.authalic_radius(), abs=1e-4)
    assert 6371000.7900 == pytest.approx(wgs84.volumetric_radius(), abs=1e-4)


def test_system_operators():
    """Test operators"""
    wgs84 = core.geodetic.System()
    # https://en.wikipedia.org/wiki/Geodetic_Reference_System_1980
    grs80 = core.geodetic.System(6378137, 1 / 298.257222101)
    assert 6378137 == pytest.approx(grs80.semi_major_axis)
    assert 1 / 298.257222101 == pytest.approx(grs80.flattening)
    assert wgs84 == wgs84
    assert wgs84 != grs80


def test_system_pickle():
    """Serialization test"""
    wgs84 = core.geodetic.System()
    assert wgs84 == pickle.loads(pickle.dumps(wgs84))


def test_coordinates_ecef_lla():
    """ECEF/LLA Conversion Test"""
    lon, lat, alt = core.geodetic.Coordinates(None).ecef_to_lla(
        [1176498.769459714], [5555043.905503586], [2895446.8901510699])
    assert lon[0] == pytest.approx(78.042068, abs=1e-8)
    assert lat[0] == pytest.approx(27.173891, abs=1e-8)
    assert alt[0] == pytest.approx(168.0, abs=1e-8)


def test_coordinates_lla_to_ecef():
    """LLA/ECEF Conversion Test"""
    x, y, z = core.geodetic.Coordinates(None).lla_to_ecef([78.042068],
                                                          [27.173891], [168.0])
    assert x[0] == pytest.approx(1176498.769459714, abs=1e-8)
    assert y[0] == pytest.approx(5555043.905503586, abs=1e-8)
    assert z[0] == pytest.approx(2895446.8901510699, abs=1e-8)


def test_coordinates_round_trip():
    """Check algorithm precision"""
    lon1 = np.random.uniform(-180.0, 180.0, 1000000)
    lat1 = np.random.uniform(-90.0, 90.0, 1000000)
    alt1 = np.random.uniform(-10000, 100000, 1000000)

    a = core.geodetic.Coordinates(None)
    b = core.geodetic.Coordinates(None)

    lon2, lat2, alt2 = a.transform(b, lon1, lat1, alt1, num_threads=0)

    assert 0 == pytest.approx((lon1 - lon2).mean(), abs=1e-12)
    assert 0 == pytest.approx((lat1 - lat2).mean(), abs=1e-12)
    assert 0 == pytest.approx((alt1 - alt2).mean(), abs=1e-10)


def test_coordinates_pickle():
    """Serialization test"""
    a = core.geodetic.Coordinates(None)
    b = pickle.loads(pickle.dumps(a))
    assert np.all(a.__getstate__() == b.__getstate__())


def test_point():
    """Test construction and accessors of the object"""
    pt = core.geodetic.Point(12, 24)
    assert pt.lon == 12
    assert pt.lat == 24
    assert str(pt) == "(12, 24)"
    assert repr(pt) == "(12, 24)"
    pt.lon = 55
    assert pt.lon == 55
    pt.lat = 33
    assert pt.lat == 33
    point = core.geodetic.Point.read_wkt("POINT(-2 2)")
    assert point.wkt() == "POINT(-2 2)"


def test_point_distance():
    acropolis = core.geodetic.Point(23.725750, 37.971536)
    ulb = core.geodetic.Point(4.3826169, 50.8119483)
    assert 2088389.07865908 == pytest.approx(acropolis.distance(
        ulb, strategy="andoyer"),
                                             abs=1e-6)
    assert 2088384.36439399 == pytest.approx(acropolis.distance(
        ulb, strategy="thomas"),
                                             abs=1e-6)
    assert 2088384.36606831 == pytest.approx(acropolis.distance(
        ulb, strategy="vincenty"),
                                             abs=1e-6)
    assert acropolis.distance(ulb,
                              strategy="thomas") == acropolis.distance(ulb)
    with pytest.raises(ValueError):
        acropolis.distance(ulb, strategy="Thomas")



def test_point_pickle():
    """Serialization tests"""
    a = core.geodetic.Point(1, 2)
    b = pickle.loads(pickle.dumps(a))
    assert a.lon == b.lon
    assert a.lat == b.lat
    assert a == b
    assert not a != b
    assert id(a) != id(b)


def test_box():
    """Test construction and accessors of the object"""
    min_corner = core.geodetic.Point(0, 1)
    max_corner = core.geodetic.Point(2, 3)

    box = core.geodetic.Box(min_corner, max_corner)
    assert str(box) == "((0, 1), (2, 3))"
    assert box.min_corner.lon == 0
    assert box.min_corner.lat == 1
    assert box.max_corner.lon == 2
    assert box.max_corner.lat == 3

    assert box.distance(box) == 0
    assert box.distance(min_corner) == 0
    assert box.distance(core.geodetic.Point(1, 1)) != 0

    assert box.covered_by(min_corner)
    assert box.covered_by(max_corner)
    assert box.covered_by(core.geodetic.Point(1, 2))
    assert not box.covered_by(core.geodetic.Point(0, 0))

    flags = box.covered_by([1, 0], [2, 0])
    assert np.all(flags == [1, 0])

    box.min_corner, box.max_corner = max_corner, min_corner
    assert box.min_corner.lon == 2
    assert box.min_corner.lat == 3
    assert box.max_corner.lon == 0
    assert box.max_corner.lat == 1

    assert box.wkt() == "POLYGON((2 3,2 1,0 1,0 3,2 3))"
    box = core.geodetic.Box.read_wkt("POLYGON((2 3,2 1,0 1,0 3,2 3))")
    assert repr(box) == "((2, 3), (0, 1))"

    box = core.geodetic.Box.whole_earth()
    assert repr(box) == "((-180, -90), (180, 90))"


def test_box_pickle():
    """Serialization tests"""
    min_corner = core.geodetic.Point(0, 1)
    max_corner = core.geodetic.Point(2, 3)
    a = core.geodetic.Box(min_corner, max_corner)
    b = pickle.loads(pickle.dumps(a))
    assert a.min_corner.lon == b.min_corner.lon
    assert a.min_corner.lat == b.min_corner.lat
    assert a.max_corner.lon == b.max_corner.lon
    assert a.max_corner.lat == b.max_corner.lat
    assert a == b
    assert not a != b


def test_polygon():
    polygon = core.geodetic.Polygon.read_wkt("POLYGON((0 0,0 7,4 2,2 0,0 0))")
    assert repr(polygon) == "(((0, 0), (0, 7), (4, 2), (2, 0), (0, 0)))"
    assert polygon.envelope() == core.geodetic.Box(core.geodetic.Point(0, 0),
                                                   core.geodetic.Point(4, 7))
    polygon = core.geodetic.Polygon([
        core.geodetic.Point(0, 0),
        core.geodetic.Point(0, 5),
        core.geodetic.Point(5, 5),
        core.geodetic.Point(5, 0),
        core.geodetic.Point(0, 0)
    ], [[
        core.geodetic.Point(1, 1),
        core.geodetic.Point(4, 1),
        core.geodetic.Point(4, 4),
        core.geodetic.Point(1, 4),
        core.geodetic.Point(1, 1)
    ]])
    assert polygon.distance(polygon) == 0
    assert polygon.distance(core.geodetic.Point(0, 0)) == 0
    assert polygon.distance(core.geodetic.Point(10, 10)) != 0

    assert repr(polygon) == "(((0, 0), (0, 5), (5, 5), (5, 0), (0, 0)), " \
        "((1, 1), (4, 1), (4, 4), (1, 4), (1, 1)))"
    assert polygon.wkt() == "POLYGON((0 0,0 5,5 5,5 0,0 0)," \
        "(1 1,4 1,4 4,1 4,1 1))"


def test_polygon_pickle():
    for item in [
            "POLYGON((0 0,0 7,4 2,2 0,0 0))",
            "POLYGON((0 0,0 5,5 5,5 0,0 0),(1 1,4 1,4 4,1 4,1 1))"
    ]:
        polygon = core.geodetic.Polygon.read_wkt(item)
        other = pickle.loads(pickle.dumps(polygon))
        assert polygon == other
        assert not polygon != other
        assert id(polygon) != id(other)


def test_polygon_covered_by():
    lon = np.arange(0, 360, 10)
    lat = np.arange(-90, 90.5, 10)
    mx, my = np.meshgrid(lon, lat)
    polygon = core.geodetic.Polygon(
        [core.geodetic.Point(*item) for item in POINTS])
    mask1 = polygon.covered_by(mx.flatten(), my.flatten()).reshape(mx.shape)
    mask2 = polygon.covered_by(mx.flatten(), my.flatten(),
                               num_theads=1).reshape(mx.shape)
    assert np.all(mask2 == mask1)
    ix, iy = np.where(mask1 == 1)
    assert np.all(ix == [
        4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 7,
        7, 7, 7, 7, 7, 8, 8, 8, 8, 8
    ])
    assert np.all(iy == [
        0, 1, 30, 31, 32, 33, 34, 35, 0, 1, 30, 31, 32, 33, 34, 35, 0, 1, 31,
        32, 33, 34, 35, 0, 1, 32, 33, 34, 35, 0, 1, 33, 34, 35
    ])
    # Switch to [-180, 180[ input range
    mx = (mx + 180) % 360 - 180
    mask2 = polygon.covered_by(mx.flatten(), my.flatten()).reshape(mx.shape)
    assert np.all(mask2 == mask1)


def test_coordinate_distance():
    lon = np.arange(0, 360, 10)
    lat = np.arange(-90, 90.5, 10)
    mx, my = np.meshgrid(lon, lat)
    d1 = core.geodetic.coordinate_distances(mx.flatten(), my.flatten(),
                                       mx.flatten() + 1,
                                       my.flatten() + 1,
                                       strategy="vincenty", num_threads=1)
    d0 = core.geodetic.coordinate_distances(mx.flatten(), my.flatten(),
                                       mx.flatten() + 1,
                                       my.flatten() + 1,
                                       strategy="vincenty", num_threads=0)
    assert np.all(d0 == d1)
    d0 = d0.reshape(mx.shape)
    for iy in range(d0.shape[0]):
        assert np.all(np.abs((d0[iy, :] - d0[iy, 0]) <= 1e-6))
    for ix in range(d0.shape[1]):
        print(d0[:, ix], d0[0, ix])
        delta = np.abs(d0[:, ix] - d0[0, ix])
        assert np.all(delta[delta != 0] > 1e3)