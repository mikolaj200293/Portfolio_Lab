document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;
      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      const summary = document.querySelector('div.summary');
      const checkboxes = Array.from(document.querySelectorAll('input[name=categories]'));
      const organizations = Array.from(document.querySelectorAll('input[name=organization]'));
      const numberOfBagsInput = document.querySelector('input[name="bags"]');
      const street = document.querySelector('input[name="address"]').value;
      const city = document.querySelector('input[name="city"]').value;
      const postcode = document.querySelector('input[name="postcode"]').value;
      const phone = document.querySelector('input[name="phone"]').value;
      const data = document.querySelector('input[name="data"]').value;
      const time = document.querySelector('input[name="time"]').value;
      const additionalInfo = document.querySelector('textarea[name="more_info"]').value;

      if (this.currentStep === 2) {
        const selectedCategory = checkboxes.filter(function (element, index, array) {
        return element.checked
        });
        organizations.forEach(el => {
        const foundationName = el.parentElement.children[2].children[0].innerHTML;
        const JSONFoundation = institutions.filter(function (element, index, array) {
          return element.name === foundationName
        });
        const foundationCategory = JSONFoundation[0].categories;
        if (foundationCategory !== parseInt(selectedCategory[0].attributes[2].value)) {
          el.parentElement.style.display = "none";
        }
        });
        summary.children[0].children[1].children[0].children[1].innerHTML = `Przekazujesz ${selectedCategory[0].parentElement.children[2].innerHTML}. `;
        }

      if (this.currentStep === 3) {
        summary.children[0].children[1].children[0].children[1].innerHTML += `Ilość worków: ${numberOfBagsInput.value}`;
      }

      if (this.currentStep === 4) {
        const selectedInstitution = organizations.filter(function (element, index, array) {
        return element.checked
        });
        summary.children[0].children[1].children[1].children[1].innerHTML = `Dla ${selectedInstitution[0].parentElement.children[2].firstElementChild.innerHTML}`;
      }

      if (this.currentStep === 5) {
        summary.children[1].children[0].children[1].children[0].innerHTML = street;
        summary.children[1].children[0].children[1].children[1].innerHTML = city;
        summary.children[1].children[0].children[1].children[2].innerHTML = postcode;
        summary.children[1].children[0].children[1].children[3].innerHTML = phone;
        summary.children[1].children[0].children[1].children[0].innerHTML = street;
        summary.children[1].children[1].children[1].children[0].innerHTML = data;
        summary.children[1].children[1].children[1].children[1].innerHTML = time;
        summary.children[1].children[1].children[1].children[2].innerHTML = additionalInfo;
      }

      if (this.currentStep === 6) {
        this.submit(event);
        const selectedCategory = checkboxes.filter(function (element, index, array) {
        return element.checked
      });
        const category = selectedCategory[0].attributes[2].value;
        const quantity = document.querySelector('input[name="bags"]').value;
        const selectedInstitution = organizations.filter(function (element, index, array) {
        return element.checked
      });
        const institution = selectedInstitution[0].parentElement.children[2].firstElementChild.innerHTML;
        const csrftoken_hidden = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
      const csrftoken = getCookie('csrftoken');

        fetch('http://127.0.0.1:8000/add_donation', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({
            'csrfmiddlewaretoken': csrftoken_hidden,
            'bags': quantity,
            'categories': category,
            'organization': institution,
            'address': street,
            'phone': phone,
            'city': city,
            'postcode': postcode,
            'data': data,
            'time': time,
            'more_info': additionalInfo
          })
        }).then(res => res.json())
          .then(res => window.location.replace(`http://127.0.0.1:8000${res['url']}`));
      }


      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

      const archive_button = document.querySelectorAll('.archive-donation')

        function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      }
      const csrftoken = getCookie('csrftoken');

      archive_button.forEach((el, index) => {
        const donation = document.querySelector(`#donation-${index + 1}`)
        if (donations[index].is_taken === true) {
            donation.style.color = "grey"
            donation.className = "strike"
          }
        el.addEventListener('click', function (e) {
          let is_taken = true
          if (donations[index].is_taken === true) {
            is_taken = false
          }
          const donation_id = donations[index].id
          fetch('http://127.0.0.1:8000/profile', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify({
            "donation_id": donation_id,
            "is_taken": is_taken,
          })
        }).then(res => res.json())
          .then(res => window.location.replace(`http://127.0.0.1:8000${res['url']}`));
        })
      })
});

