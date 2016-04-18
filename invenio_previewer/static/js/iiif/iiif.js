/*
 * This file is part of Invenio.
 * Copyright (C) 2016 CERN.
 *
 * Invenio is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * Invenio is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Invenio; if not, write to the Free Software Foundation, Inc.,
 * 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
 */

$(function (){
  'use strict';

  // Fetch the gallery from HTML data attributes
  var gallery = [];
  $("#gallery-data").children("div").each(function() {
    var filename = $(this).data("filename");
    var url = $(this).data("url");
    gallery.push({filename: filename, url: url});
  });

  var openSeadragonOptions = {
    id: "openseadragon-viewer",

    // Style
    showNavigator: true,

    // Buttons
    zoomInButton: "zoom-in",
    zoomOutButton: "zoom-out",
    homeButton: "home",
    nextButton: "next",
    previousButton: "previous",

    // We have a custom fullscreen button that uses fullscreen.js
    showFullPageControl: false,

    // Content
    prefixUrl: "/osd/images/",
    initialPage: $("#gallery-data").data("first-image-index"),
    sequenceMode: gallery.length > 1,
    tileSources: $.map(gallery, function(v) { return v.url; })
  };

  var viewer = OpenSeadragon(openSeadragonOptions);

  // Resizes the OSD viewer to fill its container
  function resizeViewer() {
    var screenWidth = window.innerWidth;
    var screenHeight = window.innerHeight;
    var headerHeight = $("#viewer-header").height();
    $("#openseadragon-viewer").width(screenWidth);
    $("#openseadragon-viewer").height(screenHeight - headerHeight);
  }

  // Add event handlers to update UI elements on errors, page changes, etc.
  viewer.addHandler("tile-load-failed", function (data){
    $("#viewer-error").show();
    $("#viewer-spinner").hide();
    resizeViewer();
  });
  viewer.addHandler("open-failed", function (data){
    $("#viewer-error").show();
    $("#viewer-spinner").hide();
    resizeViewer();
  });
  viewer.addHandler("page", function (data){
    $("#current-file").text(gallery[data.page].filename);
    $("#current-page").text(data.page + 1);
    $("#viewer-error").hide();
    $("#viewer-spinner").show();
  });
  viewer.addHandler("tile-loaded", function (data){
    $("#viewer-error").hide();
    $("#viewer-spinner").hide();
    resizeViewer();
  });

  $(window).resize(resizeViewer);
});
