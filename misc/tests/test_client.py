#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
unittest for Clarifai API Python Client
"""

import os
import hashlib
import unittest
from clarifai.client import ClarifaiApi

class TestClarifaiApi(unittest.TestCase):
  """
  test the Clarifai API Python client with all supported features
  """

  def test_api_connection(self):
    api = ClarifaiApi()
    self.assertTrue(api)

  def test_get_info(self):
    api = ClarifaiApi()
    response = api.get_info()
    self.assertTrue(response.get('api_version'))
    self.assertTrue(len(response) > 0)

  def test_tag_one_image(self):
    """ tag one image, from url and disk """
    # tag image from online URL
    image_url = 'http://clarifai-img.s3.amazonaws.com/test/toddler-flowers.jpeg'
    api = ClarifaiApi()
    response = api.tag_image_urls(image_url)
    self.assertTrue(response)
    self.assertTrue(response['results'][0]['url'] == image_url)

    # tag image from local fs
    image_file = 'tests/data/toddler-flowers.jpeg'
    api = ClarifaiApi()
    if os.path.exists(image_file):
      with open(image_file, 'rb') as fb:
        response = api.tag_images(fb)
        self.assertTrue(response)

  def test_tag_images(self):
    """ tag multiple images, from url and disk """
    # tag images from online URL
    image_url_base = 'http://clarifai-img.s3.amazonaws.com/test'
    image_files = ['metro-north.jpg', 'octopus.jpg', 'tahoe.jpg', 'thai-market.jpg']
    image_urls = [os.path.join(image_url_base, one_file) for one_file in image_files]

    api = ClarifaiApi()
    response = api.tag_image_urls(image_urls)
    self.assertTrue(response)

    # tag images frmo local fs
    image_dir = 'tests/data'
    image_files = ['metro-north.jpg', 'octopus.jpg', 'tahoe.jpg', 'thai-market.jpg']

    api = ClarifaiApi()
    if os.path.exists(image_dir):
      image_files = [open(os.path.join(image_dir, one_file), 'rb') for one_file in image_files]
      response = api.tag_images(image_files)
      self.assertTrue(response)
      for fd in image_files:
        fd.close()

  def test_unicode_urls(self):
    image_url = u'http://www.alvaronoboa.com/wp-content/uploads/2013/02/Álvaro-Noboa-y-Annabella-Azín-Votaciones-41-1024x682.jpg'

    api = ClarifaiApi()
    response = api.tag_image_urls(image_url)
    self.assertTrue(response)
    self.assertTrue(response['results'][0]['url'] == image_url)

  def test_tag_gif(self):
    """ tag one GIF animation file """
    # source: http://media.giphy.com/media/fRZn2vraBGiA0/giphy.gif
    image_url = 'http://media.giphy.com/media/fRZn2vraBGiA0/giphy.gif'

    api = ClarifaiApi()
    response = api.tag_image_urls(image_url)
    self.assertTrue(response)
    self.assertTrue(response['results'][0]['url'] == image_url)

    image_file = 'tests/data/water-ocean-turtle.gif'
    api = ClarifaiApi()
    if os.path.exists(image_file):
      with open(image_file, 'rb') as fb:
        response = api.tag_images(fb)
        self.assertTrue(response)

  def test_tag_one_video(self):
    # video source: http://techslides.com/demos/sample-videos/small.mp4
    video_url = 'http://techslides.com/demos/sample-videos/small.mp4'

    api = ClarifaiApi()
    response = api.tag_image_urls(video_url)
    self.assertTrue(response)
    self.assertTrue(response['results'][0]['url'] == video_url)

  def test_tag_one_video_from_localfs(self):
    # video source: http://techslides.com/demos/sample-videos/small.mp4
    video_file = 'tests/data/small.mp4'
    api = ClarifaiApi()
    if os.path.exists(video_file):
      with open(video_file, 'rb') as fb:
        response = api.tag_images(fb)
        self.assertTrue(response)

  def test_embed_one_image(self):
    image_url = 'http://clarifai-img.s3.amazonaws.com/test/toddler-flowers.jpeg'
    api = ClarifaiApi()
    response = api.embed_image_urls(image_url)
    self.assertTrue(response)
    self.assertTrue(response['results'][0]['url'] == image_url)

  def test_embed_one_image_from_localfs(self):
    image_file = 'tests/data/toddler-flowers.jpeg'
    api = ClarifaiApi()
    if os.path.exists(image_file):
      with open(image_file, 'rb') as fb:
        response = api.embed_images(fb)
        self.assertTrue(response)

  def test_tag_n_embed_one_image(self):
    image_url_base = 'http://clarifai-img.s3.amazonaws.com/test'
    image_files = ['metro-north.jpg', 'octopus.jpg', 'tahoe.jpg', 'thai-market.jpg']
    image_urls = [os.path.join(image_url_base, one_file) for one_file in image_files]

    api = ClarifaiApi()
    response = api.tag_and_embed_image_urls(image_urls)
    self.assertTrue(response)

  def test_tag_n_embed_from_localfs(self):
    image_dir = 'tests/data'
    image_files = ['metro-north.jpg', 'octopus.jpg', 'tahoe.jpg', 'thai-market.jpg']

    api = ClarifaiApi()
    if os.path.exists(image_dir):
      image_files = [open(os.path.join(image_dir, one_file), 'rb') for one_file in image_files]
      response = api.tag_and_embed_images(image_files)
      self.assertTrue(response)
      for fd in image_files:
        fd.close()

  def test_send_feedback(self):
    """ test sending various feedback """

    urls = ['http://clarifai-img.s3.amazonaws.com/test/metro-north.jpg', \
            'http://clarifai-img.s3.amazonaws.com/test/metro-north.jpg', \
            'http://clarifai-img.s3.amazonaws.com/test/octopus.jpg']

    api = ClarifaiApi()

    response = api.feedback(urls=urls[0], add_tags='train')
    self.assertTrue(response)

    response = api.feedback(urls=urls[0], remove_tags='speed,test')
    self.assertTrue(response)

    response = api.feedback(urls=urls[0], add_tags='train', remove_tags='speed,test')
    self.assertTrue(response)

    docids = [hashlib.md5(url.encode('utf-8')).hexdigest() for url in urls]

    response = api.feedback(urls=urls[:2], similar_docids=docids[:2])
    self.assertTrue(response)

    response = api.feedback(urls=urls[1:], dissimilar_docids=docids[1:])
    self.assertTrue(response)

    response = api.feedback(urls=urls, similar_docids=docids[:2], dissimilar_docids=docids[1:])
    self.assertTrue(response)

if __name__ == '__main__':
  unittest.main()

