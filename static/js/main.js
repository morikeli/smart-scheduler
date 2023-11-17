(function() {
	"use strict";

	// Easy selector helper function
	const select = (el, all = false) => {
		el = el.trim()
		if (all) {
			return [...document.querySelectorAll(el)]
		} else {
			return document.querySelector(el)
		}
	}

	// Easy event listener function
	const on = (type, el, listener, all = false) => {
		if (all) {
			select(el, all).forEach(e => e.addEventListener(type, listener))
		} else {
			select(el, all).addEventListener(type, listener)
		}
	}

	// Easy on scroll event listener 
	const onscroll = (el, listener) => {
		el.addEventListener('scroll', listener)
	}

	// sidebar toggle
	if (select('.toggle-sidebar-btn')) {
		on('click', '.toggle-sidebar-btn', function(e) {
			select('body').classList.toggle('toggle-sidebar')
		})

		select('body').classList.add('toggle-sidebar');
	}

	// Search bar toggle
	if (select('.search-bar-toggle')) {
		on('click', '.search-bar-toggle', function(e) {
			select('.search-bar').classList.toggle('search-bar-show')
		})
	}

	// Toggle .header-scrolled class to #header when page is scrolled
	let selectHeader = select('#header')
	if (selectHeader) {
		const headerScrolled = () => {
			if (window.scrollY > 100) {
				selectHeader.classList.add('header-scrolled')
			} else {
				selectHeader.classList.remove('header-scrolled')
			}
		}
		window.addEventListener('load', headerScrolled)
		onscroll(document, headerScrolled)
	}

	// back to top button
	let backtotop = select('.back-to-top')
	if (backtotop) {
		const toggleBacktotop = () => {
		if (window.scrollY > 100) {
			backtotop.classList.add('active')
		} else {
			backtotop.classList.remove('active')
		}
		}
		window.addEventListener('load', toggleBacktotop)
		onscroll(document, toggleBacktotop)
	}

	// Preloader
	let preloader = select('#preloader');
	if (preloader) {
		window.addEventListener('load', () => {
			preloader.remove()
		});
	}

})();