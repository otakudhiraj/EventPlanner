document.addEventListener('DOMContentLoaded', function () {
    profileDropDown();
    removeAlertMessages();

    const bookNowBtn = document.querySelector("#bookNowBtn");
    if (bookNowBtn) {
        bookNowBtn.addEventListener("click", function () {
            const vegPrice = bookNowBtn.getAttribute("data-veg-price");
            const nonVegPrice = bookNowBtn.getAttribute("data-non-veg-price");
            const bookingModal = document.getElementById('bookingModal');

            openModal(bookingModal);
            bookNow(vegPrice, nonVegPrice);
        })
    }
})


function profileDropDown() {
    const profileContainer = document.querySelector('#profile-dropdown-btn');
    if (profileContainer) {
        profileContainer.addEventListener('click', function () {
            const dropdown = document.querySelector('#profile-dropdown-menu');
            dropdown.classList.toggle('hidden');
            this.parentElement.classList.toggle("bg-secondary");
        });
    }
}

function removeAlertMessages() {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        const messages = messageContainer.querySelectorAll('[id^="message-"]');
        messages.forEach((message, index) => {
            setTimeout(() => {
                message.classList.remove('opacity-100');
                message.classList.add('opacity-0');
                setTimeout(() => {
                    message.remove();
                }, 1000);
            }, index * 3000);
        });
    }
}

function bookNow(vegPrice, nonVegPrice) {
    const bookingModal = document.getElementById('bookingModal');
    const bookNowBtn = document.getElementById('bookNowBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const bookingForm = document.getElementById('bookingForm');


    closeModalBtn.addEventListener('click', function () {
        closeModal(bookingModal);
    });

    const totalPeopleInput = document.getElementById('total_people');
    const mealTypeSelect = document.getElementById('meal_type');
    const priceDisplay = document.getElementById('pricePerPerson');
    const totalAmountDisplay = document.getElementById('totalAmount');

    function updateTotalAmount() {
        const totalPeople = totalPeopleInput.value;
        const mealType = mealTypeSelect.value;
        let pricePerPerson = 0;

        if (mealType === 'Vegetarian') {
            pricePerPerson = Number(vegPrice);
        } else if (mealType === 'Non-Vegetarian') {
            pricePerPerson = Number(nonVegPrice);
        }

        priceDisplay.textContent = pricePerPerson.toFixed(2);
        const totalAmount = totalPeople * pricePerPerson;
        totalAmountDisplay.textContent = totalAmount.toFixed(2);
    }

    totalPeopleInput.addEventListener('input', updateTotalAmount);
    mealTypeSelect.addEventListener('change', updateTotalAmount);

    updateTotalAmount();

    bookingForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Show loading state
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = 'Booking...';

        try {
            const csrfToken = this.querySelector("[name=csrfmiddlewaretoken]").value;
            const formData = {
                total_people: this.total_people.value,
                meal_type: this.meal_type.value,
                venue: this.venue.value,
                user: this.user.value
            };

            const response = await fetch(this.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.errors || 'Booking failed');
            }

            // Success handling
            closeModal(bookingModal);

            const paymentModal = document.getElementById('paymentModal');

            openModal(paymentModal);
            pay();

        } catch (error) {
            console.error('Booking error:', error);
            alert(`Error: ${error.message}`);
        } finally {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Confirm Booking';
        }

        closeModal(bookingModal);
    });
}

function openModal(modal) {
    let body = document.body;
    modal.classList.remove('hidden');
    body.style.overflow = 'hidden';
    body.style.position = 'fixed';
    body.style.width = '100%';
}

function closeModal(modal) {
    let body = document.body;
    modal.classList.add('hidden');
    body.style.overflow = '';
    body.style.position = '';
    body.style.width = '';
}

function pay() {
    const paymentModal = document.querySelector("#paymentModal");
    document.querySelectorAll('.payment-option').forEach(option => {
        option.addEventListener('click', function () {
            const paymentMethod = this.textContent.trim();
            alert(`Selected payment method: ${paymentMethod}`);
            closeModal(paymentModal);
        });
    });
}
