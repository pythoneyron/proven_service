window.addEventListener('load', () => {

  /*** Скрипт карусели "фото товара" ***/
  let chevron_left = document.querySelector('.chevron_left')
  let chevron_right = document.querySelector('.chevron_right')
  let list_img = document.querySelector('.wrap_list_img')

  chevron_right.addEventListener('click', move_right)
  chevron_right.addEventListener('touch', move_right)
  chevron_left.addEventListener('click', move_left)
  chevron_left.addEventListener('touch', move_left)

  function move_right (e) {
    e.preventDefault()
    list_img.scrollLeft += 40
  }

  function move_left (e) {
    e.preventDefault()
    list_img.scrollLeft -= 40
  }

  /*
   В css есть вот такое свойство отвечающее за плавность движения
   Не кроссбраузерно, но много чего поддерживает
   scroll-behavior: smooth;
   */

  /*** Скрипт подстановки изображения в большой блок ***/
  let arr_img = document.querySelectorAll('.list_img li img')
  let big_img = document.getElementById('big_img')
  for (let i = 0; i < arr_img.length; i++) {
    arr_img[i].addEventListener('click', substitute_image)
    arr_img[i].addEventListener('touch', substitute_image)
  }

  function substitute_image (e) {
    big_img.setAttribute('src', e.target.src)
  }

  /*** Скрипт работы с табами ***/
  let tab = document.querySelectorAll('.tabs h3')
  let tab_content = document.querySelectorAll('.tab_content')

  for (let i = 0; i < tab.length; i++) {
    tab[i].addEventListener('click', switch_func)
    tab[i].addEventListener('touch', switch_func)
  }

  function switch_func (e) {
    for (let i = 0; i < tab.length; i++) {
      tab[i].classList.remove('active_tab')
      tab_content[i].removeAttribute('id')
    }
    e.currentTarget.classList.add('active_tab')
    let i = e.currentTarget.dataset.tab
    tab_content[i].setAttribute('id', 'active_content_tab')
  }

  /*** Эмуляция клика ***/
  let wrap_inp = document.querySelector('.wrap_inp')
  wrap_inp.addEventListener('click', emulateClick)
  function emulateClick () {
    let target = document.getElementById('file-input')
    console.log(target)
    let click = new CustomEvent('click')
    target.dispatchEvent(click)
  }

  /*** Скрыть показать форму, - мой отзыв  ***/
  let write_feedback = document.getElementById('write_feedback')
  write_feedback.addEventListener('click', hide_all_func)
  function hide_all_func (e) {
    e.preventDefault()
    let card_section = document.querySelector('.card-section')
    card_section.style.display = 'none'
    let my_review = document.querySelector('.my_review')
    my_review.style.display = 'block'
    document.body.scrollTop = document.documentElement.scrollTop = 0
  }

  let my_review1 = document.querySelector('.my_review')
  my_review1.addEventListener('click', view_all_func1)
  function view_all_func1 (e) {
    // e.preventDefault()
    if (e.target.tagName === 'A') {
      let card_section = document.querySelector('.card-section')
      card_section.style.display = 'block'
      my_review1.style.display = 'none'
    }
  }

  /*** Оранжевая кнопка на мобильной версии ***/
  //let back_card = document.querySelector('')

  /***  Скрипт карусели "С этим товаром смотрят"  ***/
  let btn_left = document.getElementById('btn_left')
  let btn_right = document.getElementById('btn_right')
  let list_card = document.querySelector('.wrap-product-look__card')

// Ширина карточки 192 + (16 * 2) = 224px
  let qty_card = list_card.length

  btn_right.addEventListener('click', move_right_carusel)
  btn_right.addEventListener('touch', move_right_carusel)
  btn_left.addEventListener('click', move_left_carusel)
  btn_left.addEventListener('touch', move_left_carusel)

  function move_right_carusel (e) {
    e.preventDefault()
    list_card.scrollLeft += 192
  }

  function move_left_carusel (e) {
    e.preventDefault()
    list_card.scrollLeft -= 100
  }

  /*** Выбор звезды ***/
  class WorkStar {
    constructor (stars_input, select_star) {
      this.stars_input = stars_input // инпут куда будем выводить количество звезд
      this.select_star = select_star // html список тегов i со звездами
      this.num = 0 // Количество звезд
      this.addEventClick()
      this.addEventMouseOver()
    }

    addEventClick () {
      for (let i = 0; i < this.select_star.length; i++) {
        this.select_star[i].addEventListener('click', (e) => this.select_stars.call(this, e.target))
      }
    }

    addEventMouseOver () {
      for (let i = 0; i < this.select_star.length; i++) {
        this.select_star[i].addEventListener('mouseover', (e) => this.select_star_hover.call(this, e.target))
      }
    }

    select_stars (e) {
      this.num = e.dataset.qtyStar
      this.celebrate_stars.call(this)
    }

    select_star_hover (e) {
      this.num = e.dataset.qtyStar
      this.celebrate_stars.call(this)
    }

    celebrate_stars () {
      for (let i = 0; i < this.select_star.length; i++) {
        if (i < this.num) {
          this.select_star[i].setAttribute('class', 'fill star')
        } else {
          this.select_star[i].setAttribute('class', 'empty star')
        }
      }
      this.stars_input.value = +this.num

      switch (this.num) {
        case '1':
          this.stars_input.value = '1'
          break
        case '2':
          this.stars_input.value = '2'
          break
        case '3':
          this.stars_input.value = '3'
          break
        case '4':
          this.stars_input.value = '4'
          break
        case '5':
          this.stars_input.value = '5'
          break
        default:
          this.stars_input.value = '0'
      }
    }
  }

  let stars_input1 = document.getElementById('stars_input1')
  let select_star1 = document.querySelectorAll('#stars1 i')
  let generalSelectStars1 = new WorkStar(stars_input1, select_star1)

  let stars_input2 = document.getElementById('stars_input2')
  let select_star2 = document.querySelectorAll('#stars2 i')
  let generalSelectStars2 = new WorkStar(stars_input2, select_star2)

  let stars_input3 = document.getElementById('stars_input3')
  let select_star3 = document.querySelectorAll('#stars3 i')
  let generalSelectStars3 = new WorkStar(stars_input3, select_star3)

  /*** Переставляем два блока, - "Преимущества и Краткая информация." ***/

  update_place()

  let screen_width = window.innerWidth
  window.addEventListener('resize', (e) => {
    let res = screen_width - e.target.innerWidth
    if (res > 5) {
      update_place()
    }
    if (res < -5) {
      update_place()
    }
  })

  function update_place () {
    let width = window.innerWidth
    if (width < 1240) {
      let wrap_benefits_brief = document.querySelector('.wrap_benefits_brief-information').cloneNode(true)
      document.querySelector('.wrap_benefits_brief-information').remove()
      let overview_specifications = document.querySelector('.overview-specifications')
      let div_card = document.querySelector('.card')
      div_card.insertBefore(wrap_benefits_brief, overview_specifications)
      let benefits_brief = document.querySelector('.wrap_benefits_brief-information')
      benefits_brief.style.flexDirection = 'row'
      benefits_brief.style.justifyContent = 'space-between'

      if (width < 1240 && width > 1023) {
        let region_point = document.querySelector('.region-point')
        let block_price__brief_information = document.querySelector('.block-price__brief-information')
        let block_price__benefits = document.querySelector('.block-price__benefits')
        block_price__brief_information.style.width = region_point.offsetWidth + 'px'
        block_price__benefits.style.width = region_point.offsetWidth + 'px'
      }

    } else {
      let wrap_benefits_brief = document.querySelector('.wrap_benefits_brief-information').cloneNode(true)
      document.querySelector('.wrap_benefits_brief-information').remove()
      let block_price = document.querySelector('.block-price')
      block_price.appendChild(wrap_benefits_brief)
      let benefits_brief = document.querySelector('.wrap_benefits_brief-information')
      benefits_brief.style.flexDirection = 'column'
      benefits_brief.style.justifyContent = 'flex-start'

      let block_price__brief_information = document.querySelector('.block-price__brief-information')
      let block_price__benefits = document.querySelector('.block-price__benefits')
      block_price__brief_information.style.width = ''
      block_price__benefits.style.width = ''
    }

    /*** Переставляем id продукта из хлебных крошек, в  изображение товара ***/
    if (width < 1024) {
      let element = document.getElementById('id_product')
      if (element) {
        let id_product = element.cloneNode(true)
        element.remove()
        id_product.classList.add('id_product')
        let container = document.querySelector('.wrap-img-price')
        let element_before = document.querySelector('.view-img-product')
        container.insertBefore(id_product, element_before)
      }
    } else if (width > 1024) {
      let element = document.getElementById('id_product')
      if (element) {
        let id_product = element.cloneNode(true)
        element.remove()
        id_product.classList.remove('id_product')
        let container = document.querySelector('.card__breadcrumbs')
        container.appendChild(id_product)
      }
    }

    /*** На мобильной версии, перенос блока с ценой и пр. под главное изображение товара ***/
    if (width < 1024) {
      let element = document.querySelector('.block-price')
      if (element) {
        let id_product = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.big-img')
        let element_before = document.querySelector('.zoom')
        container.insertBefore(id_product, element_before)
      }
    } else if (width > 1024) {
      let element = document.querySelector('.block-price')
      if (element) {
        let id_product = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.wrap-img-price')
        container.appendChild(id_product)
      }
    }

    /*** На мобильной версии, перенос ссылки под кнопку в корзину ***/
    if (width < 1024) {
      let element = document.querySelector('#icon_link')
      if (element) {
        let link = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.block-price__comparison-favorite')
        container.appendChild(link)
      }
    } else if (width > 1024) {
      let element = document.querySelector('#icon_link')
      if (element) {
        let id_product = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.card__product-name')
        container.appendChild(id_product)
      }
    }

    /*** На мобильной версии, перенос фото товара до region-point ***/
    if (width < 1024) {
      let element = document.querySelector('.view-img-product > .wrap_for_chevron')
      if (element) {
        let photo = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.block-price')
        let element_before = document.querySelector('.region-point')
        container.insertBefore(photo, element_before)
        photo.style.marginLeft = '0'
        photo.style.overflow = 'hidden'
        photo.style.display = 'inline-block'

        let class_head_photo = document.querySelector('.wrap_for_chevron > .head_photo')
        if (!class_head_photo) {
          let container_for_head = document.querySelector('.wrap_for_chevron')
          let element_befor = document.querySelector('.wrap_for_chevron > .chevron_left')
          let head_photo = document.createElement('h4')
          head_photo.innerText = 'Другие фотографии'
          head_photo.classList.add('head_photo')
          container_for_head.insertBefore(head_photo, element_befor)
        }
      }
    } else if (width > 1024) { // Ставим обратно
      let element = document.querySelector('.block-price > .wrap_for_chevron')
      if (element) {
        let photo = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.view-img-product')
        container.appendChild(photo)
        photo.style.marginLeft = ''
        photo.style.overflow = ''
        photo.style.display = ''
        document.querySelector('.head_photo') ? document.querySelector('.head_photo').remove() : ''
      }
    }

    /*** Опускаем доставку ниже преимуществ на мобиле ***/
    if (width < 1024) {

      setTimeout(() => {
        let element = document.querySelector('.region-point')
        if (element) {
          let delivery = element.cloneNode(true)
          element.remove()
          let container = document.querySelector('.card')
          let element_before = document.querySelector('.overview-specifications')
          container.insertBefore(delivery, element_before)
        }
      }, 100)

      let block_price__brief_information = document.querySelector('.block-price__brief-information')
      let block_price__benefits = document.querySelector('.block-price__benefits')
      let region_point = document.querySelector('.region-point')
      block_price__brief_information.style.width = '100%'
      block_price__benefits.style.width = '100%'
      region_point.style.width = '100%'

      if (!document.querySelector('.show_add_info')) {
        let show_add_info = document.createElement('div')
        let span_text = document.createElement('span')
        let span_arrow = document.createElement('span')
        show_add_info.classList.add('show_add_info')
        span_text.innerText = 'Показать всю информацию'
        span_arrow.classList.add('arrow_right')
        show_add_info.appendChild(span_text)
        show_add_info.appendChild(span_arrow)
        block_price__brief_information.appendChild(show_add_info)
      }

      // Добавляю тэг элемент, - "Подробнее о доставке"
      if (!document.querySelector('.show_add_delivery')) {
        let show_add_delivery = document.createElement('div')
        let span_text = document.createElement('span')
        let span_arrow = document.createElement('span')
        show_add_delivery.classList.add('show_add_delivery')
        span_text.innerText = 'Подробнее о доставке'
        span_arrow.classList.add('arrow_right')
        show_add_delivery.appendChild(span_text)
        show_add_delivery.appendChild(span_arrow)
        let point = document.querySelector('.region-point > .point')
        point.appendChild(show_add_delivery)
      }

    } else if (width > 1023) {
      setTimeout(() => {

        let element = document.querySelector('.card > .region-point')
        if (element) {
          let delivery = element.cloneNode(true)
          element.remove()
          let container = document.querySelector('.block-price')
          container.appendChild(delivery)
        }

      }, 100)

      let block_price__brief_information = document.querySelector('.block-price__brief-information')
      let block_price__benefits = document.querySelector('.block-price__benefits')
      let region_point = document.querySelector('.region-point')
      block_price__brief_information.style.width = ''
      block_price__benefits.style.width = ''
      region_point.style.width = ''

      document.querySelector('.show_add_info') ? document.querySelector('.show_add_info').remove() : ''
    }

    /*** Оставить отзыв на мобильной версии другая надпись ***/
    let back_card = document.querySelector('#back_card')

    if (width < 1024) {
      back_card.innerHTML = '<span></span> Оставить отзыв'
    } else if (width > 1023) {
      back_card.innerHTML = '<span></span> Назад'
    }

    /*** На ширине 840 - 600 Перемещаем логотип "Мир спорта вверх и обратно" ***/
    if (width < 840) {
      let element = document.querySelector('.header-middle-list .header-middle__item--1')
      if (element) {
        let logo = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.header-up__list')
        let elem_bef = document.querySelector('.your-town')
        container.insertBefore(logo, elem_bef)
      }
    } else if (width > 839) {
/*      let element = document.querySelector('.header-middle-list .header-middle__item--1')
      if (element) {
        let logo = element.cloneNode(true)
        element.remove()
        let container = document.querySelector('.header-up__list')
        let elem_bef = document.querySelector('.your-town')
        container.insertBefore(logo, elem_bef)
      }*/
    }
  }

  update_place()
})

/*** Зона добавления фото ***/
$(document).ready(function () {
  var dropZone = $('#upload-container')

  $('#file-input').focus(function () {
    $('label').addClass('focus')
  })
    .focusout(function () {
      $('label').removeClass('focus')
    })

  dropZone.on('drag dragstart dragend dragover dragenter dragleave drop', function () {
    return false
  })

  dropZone.on('dragover dragenter', function () {
    dropZone.addClass('dragover')
  })

  dropZone.on('dragleave', function (e) {
    let dx = e.pageX - dropZone.offset().left
    let dy = e.pageY - dropZone.offset().top
    if ((dx < 0) || (dx > dropZone.width()) || (dy < 0) || (dy > dropZone.height())) {
      dropZone.removeClass('dragover')
    }
  })

  dropZone.on('drop', function (e) {
    dropZone.removeClass('dragover')
    let files = e.originalEvent.dataTransfer.files
    sendFiles(files)
  })

  $('#file-input').change(function () {
    let files = this.files
    sendFiles(files)
  })

  function sendFiles (files) {
    let maxFileSize = 5242880
    let Data = new FormData()
    $(files).each(function (index, file) {
      if ((file.size <= maxFileSize) && ((file.type == 'image/png') || (file.type == 'image/jpeg'))) {
        Data.append('images[]', file)
      }
    })

    $.ajax({
      url: dropZone.attr('action'),
      type: dropZone.attr('method'),
      data: Data,
      contentType: false,
      processData: false,
      success: function (data) {
        alert('Файлы были успешно загружены!')
      }
    })
  }
})
