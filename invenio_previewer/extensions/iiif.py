# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Previews a Images through using Flask-IIIF."""

from __future__ import absolute_import, print_function

from flask import render_template, current_app
from os.path import splitext


previewable_extensions = ['jpg', 'jpeg', 'png', 'gif', 'tif']
valid_file_extensions = ['.%s' % ext for ext in previewable_extensions]


def generate_image_gallery(file):
    """Get the other image files of the file's record."""
    from invenio_iiif.utils import url_for_iiif_info
    gallery = []
    current_file = file.file['filename']
    record_files_by_name = sorted(
        file.record['files'],
        key=lambda f: f.get('filename', ''))

    for f in record_files_by_name:
        file_ext = splitext(f.get('filename', ''))[1]
        if file_ext in valid_file_extensions:
            if {'bucket', 'filename'} <= f.viewkeys():

                bucket = f['bucket']
                filename = f['filename']
                url = url_for_iiif_info(bucket=bucket, key=filename)
                if filename == current_file:
                    first_img_index = len(gallery)

                image = dict(
                    filename=f['filename'],
                    url=url)
                gallery.append(image)

    return gallery, first_img_index


def can_preview(file):
    """Determine if the given file can be previewed."""
    return (file.has_extensions(*valid_file_extensions) and
            'invenio-iiif' in current_app.extensions)


def preview(file):
    """Render appropiate template with embed flag."""
    # Check if we can make this a gallery-like image preview
    gallery, first_img_index = generate_image_gallery(file)
    return render_template(
        'invenio_previewer/iiif.html',
        file=file.file,
        gallery=gallery,
        first_img_index=first_img_index,
        js_bundles=['previewer_base_js',
                    'previewer_iiif_js',
                    'previewer_fullscreen_js'],
        css_bundles=['previewer_base_css', 'previewer_iiif_css'],
    )
