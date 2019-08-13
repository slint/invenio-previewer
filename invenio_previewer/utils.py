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

"""Invenio Previewer Utilities."""

import bleach
import cchardet
from flask import current_app


def detect_encoding(fp, default=None):
    """Detect the character encoding of a file.

    :param fp: Open Python file pointer.
    :param default: Fallback encoding to use.
    :returns: The detected encoding.

    .. note:: The file pointer is returned at its original read position.
    """
    init_pos = fp.tell()
    try:
        sample = fp.read(
            current_app.config.get('PREVIEWER_CHARDET_BYTES', 1024))
        # Result contains 'confidence' and 'encoding'
        result = cchardet.detect(sample)
        threshold = current_app.config.get('PREVIEWER_CHARDET_CONFIDENCE', 0.9)
        if result.get('confidence', 0) > threshold:
            return result.get('encoding', default)
        else:
            return default
    except Exception:
        current_app.logger.warning('Encoding detection failed.', exc_info=True)
        return default
    finally:
        fp.seek(init_pos)


def sanitize_html(value, tags=None, attributes=None):
    """Sanitize HTML.

    Use this function when you need to include unescaped HTML that contain
    user provided data.
    """
    return bleach.clean(
        value,
        tags=tags or current_app.config['PREVIEWER_ALLOWED_TAGS'],
        attributes=attributes or current_app.config['PREVIEWER_ALLOWED_ATTRS'],
        strip=True,
    ).strip()
