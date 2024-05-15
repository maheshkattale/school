/*
Template Name: Admin Template
Author: Wrappixel

File: js
*/
// ==============================================================
// Auto select left navbar
// ==============================================================

$(function () {
    "use strict";
    var url = window.location + "";
    var path = url.replace(
      window.location.protocol + "//" + window.location.host + "/",
      ""
    );
    path="/"+path

    //console.log("path", path);

    $('#sidebarnav li').each(function(index, element) {
      // Find the <a> tag within the current <li> element
      var anchor = $(element).find('a');
      var heading = $(element).find('h4');

      // Get the URL from the href attribute of the <a> tag
      var url = anchor.attr('href');
      //console.log("URL for item " + (index + 1) + ":", url);
      // Check if the current URL matches the URL of the anchor tag
      if (path === url) {
          // If they match, add the class "selected" to the anchor tag
          heading.addClass('selected');
          heading.addClass('active');
          heading.parent().parent().css('display','block');
          heading.parent().parent().parent().addClass('open');

      }
    });

    // var element = $("ul#sidebarnav a").filter(function () {
    //   return this.href === url || this.href === path; // || url.href.indexOf(this.href) === 0;
    // });
    // element.parentsUntil(".sidebar-nav").each(function (index) {
    //   if ($(this).is("li") && $(this).children("a").length !== 0) {
    //     $(this).children("a").addClass("active");
    //     $(this).parent("ul#sidebarnav").length === 0
    //       ? $(this).addClass("active")
    //       : $(this).addClass("selected");
    //   } else if (!$(this).is("ul") && $(this).children("a").length === 0) {
    //     $(this).addClass("selected");
    //   } else if ($(this).is("ul")) {
    //     $(this).addClass("in");
    //   }
    // });
  
    // element.addClass("active");
    // $("#sidebarnav a").on("click", function (e) {
    //   if (!$(this).hasClass("active")) {
    //     // hide any open menus and remove all other classes
    //     $("ul", $(this).parents("ul:first")).removeClass("in");
    //     $("a", $(this).parents("ul:first")).removeClass("active");
  
    //     // open our new menu and add the open class
    //     $(this).next("ul").addClass("in");
    //     $(this).addClass("active");
    //   } else if ($(this).hasClass("active")) {
    //     $(this).removeClass("active");
    //     $(this).parents("ul:first").removeClass("active");
    //     $(this).next("ul").removeClass("in");
    //   }
    // });
    // $("#sidebarnav >li >a.has-arrow").on("click", function (e) {
    //   e.preventDefault();
    // });
  });