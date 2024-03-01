$(document).ready(function(){
	"use strict";


  $(document).ready(function() {
    $(".pet_gallery_fig img").click(function() {
      var ExtraGallerySrc = $(this).data("src");
      $("#modal-image").attr("src", ExtraGallerySrc);
      $("#modal-box").fadeIn();
    });

    $("#modal-box .close").click(function() {
      $("#modal-box").fadeOut();
    });
  });
   /*
    ==============================================================
       Progress Bar Script Start
    ============================================================== */  
    $('.progressbar').each(function(){
      var t = $(this),
        dataperc = t.attr('data-perc'),
        barperc = Math.round(dataperc*5.56);
      t.find('.bar').animate({width:barperc}, dataperc*25);
      t.find('.label').append('<div class="perc"></div>');
      
      function perc() {
        var length = t.find('.bar').css('width'),
          perc = Math.round(parseInt(length)/5.56),
          labelpos = (parseInt(length)-2);
        t.find('.label').css('left', labelpos);
        t.find('.perc').text(perc+'%');
      }
      perc();
      setInterval(perc, 0); 
    });


    /*================================================
      pet ccompany slider start
  =================================================*/ 

  if($('.pet-ccompany-slider').length){
    $('.pet-ccompany-slider').slick({
    slidesToShow: 6,
    autoplay: true,
    arrow:false,
    cssEase: 'linear',
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 4,
            slidesToScroll:4,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        }   
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }
    

  /*================================================
      slider start
  =================================================*/ 
  
  $('.bx-pager').bxSlider({
    auto:true,
    pagerCustom: '#bx-pager'
    
  });

   /*================================================
      spinner start
  =================================================*/ 
    if($('#spinner').length){
     $( "#spinner" ).spinner();
    }



if($('.pet_about02_slider').length){
    $('.pet_about02_slider').slick({
    slidesToShow: 1,
    autoplay: true,
    arrow:false,
    autoplaySpeed: 2000,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll:1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }


  if($('.banner_fig_slider').length){
    $('.banner_fig_slider').slick({
    slidesToShow: 1,
    autoplay: true,
    fade:true,
    arrow:false,
    autoplaySpeed: 2000,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll:1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }


  if($('.pet_client02_slider').length){
    $('.pet_client02_slider').slick({
    slidesToShow: 2,
    autoplay: true,
    autoplaySpeed:5000,
    verticalSwiping: true,
    slidesToScroll: 1,
    easing: 'easeOutQuart',
    vertical: true,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 2,
            slidesToScroll:2,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
    
    
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }


if($('.pet_client03_slider').length){
    $('.pet_client03_slider').slick({
    slidesToShow: 2,
    autoplay: true,
    autoplaySpeed:5000,
    verticalSwiping: true,
    slidesToScroll: 1,
    easing: 'easeOutQuart',
    vertical: true,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 2,
            slidesToScroll:2,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
    
    
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }

  if($('.child_service_slider').length){
    $('.child_service_slider').slick({
    slidesToShow: 3,
    autoplay:true,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 2,
            slidesToScroll:2,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
    
    
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }

    /*
    ==============================================================
        DL Responsive Menu
    ==============================================================
    */
    if(typeof($.fn.dlmenu) == 'function'){
      $('#kode-responsive-navigation').each(function(){
        $(this).find('.dl-submenu').each(function(){
        if( $(this).siblings('a').attr('href') && $(this).siblings('a').attr('href') != '#' ){
          var parent_nav = $('<li class="menu-item kode-parent-menu"></li>');
          parent_nav.append($(this).siblings('a').clone());

          $(this).prepend(parent_nav);
        }
        });
        $(this).dlmenu();
      });
    }
  

   /*
    ==============================================================
        DL Responsive Menu
    ==============================================================
    */
    if(typeof($.fn.dlmenu) == 'function'){
      $('#responsive-navigation').each(function(){
        $(this).find('.dl-submenu').each(function(){
        if( $(this).siblings('a').attr('href') && $(this).siblings('a').attr('href') != '#' ){
          var parent_nav = $('<li class="menu-item kode-parent-menu"></li>');
          parent_nav.append($(this).siblings('a').clone());

          $(this).prepend(parent_nav);
        }
        });
        $(this).dlmenu();
      });
    }
	/*
	==============================================================
	 COUNTDOWN  Script Start
	==============================================================
	*/
	
	if($('.countdown').length){
		$('.countdown').downCount({ date:'8/8/2018 12:00:00', offset: +1 });
	}
 
	/*
  ==============================================================
     Counter Script Start
  ==============================================================
  */
    if($('.counter').length){
        $('.counter').counterUp({
          delay: 20,
          time: 1000
        });
    }
	
	

  /*
    =======================================================================
         Pretty Photo Script Script
    =======================================================================
  */
    if($("a[data-rel^='prettyPhoto']").length){
      $("a[data-rel^='prettyPhoto']").prettyPhoto();
    }
 

});
  
	
	jQuery(document).ready(function() {
		jQuery('.tabs .tab-links a').on('click', function(e) {
			var currentAttrValue = jQuery(this).attr('href');

			// Show/Hide Tabs
			jQuery('.tabs ' + currentAttrValue).show().siblings().hide();

			// Change/remove current tab to active
			jQuery(this).parent('li').addClass('active').siblings().removeClass('active');

			e.preventDefault();
			
			// Show/Hide Tabs
			jQuery('.tabs ' + currentAttrValue).siblings().slideUp(800);
			jQuery('.tabs ' + currentAttrValue).delay(800).slideDown(800);
			
			// Show/Hide Tabs
			jQuery('.tabs ' + currentAttrValue).fadeIn(400).siblings().hide();
		});
	});
  
// $('#demo').dcalendarpicker();
  /*
  ==============================================================
      SLICK SLIDER 
  ==============================================================
  */
  
  if($('.recent_slider').length){
    $('.recent_slider').slick({
		slidesToShow: 3,
		autoplay: true,
		autoplaySpeed: 2000,
		responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
		
		
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }

  if($('.recent_slider').length){
    $('.recent_slider').slick({
    slidesToShow: 3,
    autoplay: true,
    autoplaySpeed: 2000,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
    
    
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }
  

  if($('.pet_client_slider').length){
    $('.pet_client_slider').slick({
    slidesToShow: 5,
    autoplay: true,
    arrow:false,
    autoplaySpeed: 2000,
    responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
    
    
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }
 

   if($('.banner-slide').length){
    $('.banner-slide').slick({
		slidesToShow: 1,
		fade:true,
		responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
		
		
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
    });
  }


  


	