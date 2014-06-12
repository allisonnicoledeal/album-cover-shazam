import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2
from find_obj import filter_matches,explore_match
import itertools
from matplotlib import pyplot as plt
import numpy as np
import os


def compare_images(img1_path, img2_path):
  print img1_path
  print img2_path
  img1 = cv2.imread(img1_path, 0)
  img2 = cv2.imread(img2_path, 0)
  # print img1

  orb = cv2.ORB()

  # Find the keypoints and descriptors
  kp1, des1 = orb.detectAndCompute(img1,None)
  kp2, des2 = orb.detectAndCompute(img2,None)

  # Create BFMatcher object
  bf = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)

  try:
    matches = bf.knnMatch(des1, trainDescriptors=des2, k = 2)
    p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)

    good = []
    for m, n in matches:
      if m.distance < 0.7*n.distance:
        print n.distance
        good.append(m)

    return good
  except:
    print 'Images not similar sizes'
    print '------------------------'
    return []

def find_closest_image_match(photo_file=None):
  album_dir = './album_images'
  album_files = os.listdir(album_dir)
  album_paths = [i for i in album_files]
  if not photo_file:
    photo_dir = './img'
    photo_path = os.listdir(photo_dir)[0]
    photo_file = photo_dir + '/' + photo_path
  resize_image(photo_file)

  best_match_value = 0
  best_match_album = None
  for album_path in album_paths:
    album_file = album_dir + '/' + album_path
    good = compare_images(album_file, photo_file)
    print len(good)
    if len(good) > best_match_value:
      best_match_value = len(good)
      best_match_album = album_path

  print 'best_match_album:', best_match_album


def draw_features(img1_path, img2_path):
  print img1_path
  print img2_path
  img1 = cv2.imread(img1_path, 0)
  img2 = cv2.imread(img2_path, 0)
  print 'img1:', img1
  print 'img2:', img2

  # Initiate SIFT detector
  orb = cv2.ORB()

  # Find the keypoints and descriptors
  kp1, des1 = orb.detectAndCompute(img1,None)
  kp2, des2 = orb.detectAndCompute(img2,None)

  # Create BFMatcher object
  bf = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)

  matches = bf.knnMatch(des1, trainDescriptors=des2, k = 2)
  p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)
  explore_match('find_obj', img1,img2,kp_pairs)#cv2 shows image

  cv2.waitKey()
  # cv2.destroyAllWindows()

def resize_image(img_path, height=600, width=600):
  img = cv2.imread(img_path, 0)
  # print 'img:', img
  resized_image = cv2.resize(img, (height, width))
  cv2.imwrite(img_path, resized_image)

draw_features('./album_images/beach_boys.jpg', './img/beach_boys_photo.jpg')
find_closest_image_match('./img/florence_photo.jpg')



