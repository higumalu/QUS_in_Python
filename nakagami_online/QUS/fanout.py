'''
import numpy as np
import matplotlib.pyplot as plt

def fan_out(img, oy, angle):
    height = img.shape[0]
    width = img.shape[1]

    center_x = width // 2
    center_y = oy
    angle_range = angle * np.pi
    radius_max = min(np.sqrt(center_x**2 + center_y**2), height - 1)

    polar_coords = np.zeros((height, width, 2), dtype=int)
    polar_image = np.zeros((int(radius_max), int(angle_range * radius_max), 3))

    for y in range(height):
        for x in range(width):
            radius = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            theta = np.arctan2(y - center_y, x - center_x)
            
            polar_x = int(radius)
            polar_y = int((theta + np.pi) * radius)
            
            polar_coords[y, x] = polar_x, polar_y

    for y in range(height):
        for x in range(width):
            polar_x, polar_y = polar_coords[y, x]
            if polar_x < polar_image.shape[0] and polar_y < polar_image.shape[1]:
                polar_image[polar_x, polar_y] = img[y, x]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('Original Image')
    plt.subplot(1, 2, 2)
    plt.imshow(polar_image, cmap='gray', extent=(0, angle_range, 0, radius_max))
    plt.title('Polar Image')
    plt.xlabel('Angle (radians)')
    plt.ylabel('Radius')
    plt.tight_layout()
    plt.show()
'''

import numpy as np
import matplotlib.pyplot as plt


def scan_conversion(I, fi, m_width, m_height, m_depth):
    # I: input image
    # fi: probe angle (degree)
    # m_width: width to display
    # m_height: height to display
    # m_depth: imaging depth [mm]
    # J: output image

    m_numPt = I.shape[0]
    m_numLn = I.shape[1]

    f = m_height * 0.9 / m_depth
    Rmin = 60 * f
    Rmax = (60 + m_depth) * f

    Fi0 = np.pi * fi / 180.0
    Rdisp = m_numLn

    Hsec = Rmax - Rmin * np.cos(Fi0 / 2)
    Xd = m_width / 2.0
    Yd = Rmin * np.cos(Fi0 / 2) - (m_height - Hsec) / 2
    Yd1 = Yd + m_height - 1

    m_zeroDepthPos = Rmin - Yd

    A1 = Fi0 / 2
    A3 = (m_numPt - 1) / (Rmax - Rmin)
    A4 = (Rdisp - 1) / Fi0

    offsX = np.full((m_width, m_height), -1)
    offsY = np.full((m_width, m_height), -1)
    factor0 = np.zeros((m_width, m_height))
    factor1 = np.zeros((m_width, m_height))
    factor2 = np.zeros((m_width, m_height))
    factor3 = np.zeros((m_width, m_height))

    for y in range(1, m_height + 1):
        for x in range(1, m_width + 1):
            if Yd1 == y - 1:
                alpha = np.pi / 2
            else:
                alpha = np.arctan2(Xd - (x - 1), Yd1 - (y - 1))

            r = (Yd1 - (y - 1)) / np.cos(alpha)

            fii = A1 - alpha

            u1 = A3 * (r - Rmin)
            v1 = A4 * fii
            x2 = int(np.floor(u1))
            y2 = int(np.floor(v1))

            if 1 <= x2 < m_numPt - 1 and 1 <= y2 < Rdisp - 1:
                offsX[x - 1, y - 1] = x2
                offsY[x - 1, y - 1] = y2
                dU = u1 - x2
                dV = v1 - y2
                dUdV = dU * dV

                factor0[x - 1, y - 1] = 1 - dU - dV + dUdV
                factor1[x - 1, y - 1] = dV - dUdV
                factor2[x - 1, y - 1] = dU - dUdV
                factor3[x - 1, y - 1] = dUdV

    J = np.zeros((m_width, m_height))
    for y in range(m_height):
        for x in range(m_width):
            if offsX[x, y] != -1 and offsY[x, y] != -1:
                clr = (
                    factor0[x, y] * I[offsX[x, y], offsY[x, y]]
                    + factor1[x, y] * I[offsX[x, y] + 1, offsY[x, y]]
                    + factor2[x, y] * I[offsX[x, y], offsY[x, y] + 1]
                    + factor3[x, y] * I[offsX[x, y] + 1, offsY[x, y] + 1]
                )
                J[x, y] = clr
            else:
                J[x, y] = 0

    J = np.rot90(J, 1)

    zeroDepth_in_mm = (m_zeroDepthPos / m_height) * m_depth
    lateral_in_mm = (zeroDepth_in_mm + m_depth) * m_width / m_height
    xxx = np.arange(-lateral_in_mm / 2, lateral_in_mm / 2 + 1)
    yyy = np.arange(-zeroDepth_in_mm, m_depth + 1)

    return J, xxx, yyy



'''
image = np.random.rand(1024, 512)

img, xxx, yyy = scan_conversion(image,60,600,450,80)
plt.figure(figsize=(10, 5))

plt.imshow(img, extent=[xxx[0] / 10, xxx[-1] / 10, yyy[-1] / 10, yyy[0] / 10], cmap='viridis')
plt.colorbar()  # Add a colorbar
plt.xlabel('X (cm)')
plt.ylabel('Y (cm)')
plt.title('Polar ')
plt.tight_layout()
plt.show()
'''

