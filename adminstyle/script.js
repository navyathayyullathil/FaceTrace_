document.querySelector('.navbar-toggler').addEventListener('click', function() {
    document.querySelector('.navbar ul').classList.toggle('show');
});

    
    document.addEventListener('DOMContentLoaded', function () {
        var departmentSelect = document.getElementById('departmentSelect');
        var staffSelect = document.getElementById('staffSelect');

        departmentSelect.addEventListener('change', function () {
            // Reset staff options
            staffSelect.innerHTML = '<option disabled selected>--select staff--</option>';

            // Get selected department value
            var selectedDepartment = departmentSelect.value;

            // Add staff options based on the selected department
            if (selectedDepartment === 'option1') {
                addStaffOptions(['staff1', 'staff2', 'staff3']);
            } else if (selectedDepartment === 'option2') {
                addStaffOptions(['staff3', 'staff4', 'staff5']);
            }
        });

        function addStaffOptions(options) {
            options.forEach(function (option) {
                var optionElement = document.createElement('option');
                optionElement.value = option;
                optionElement.textContent = option;
                staffSelect.appendChild(optionElement);
            });

            // Enable the staff select
            staffSelect.disabled = false;
        }
    });

    function updateSecondDropdown() {
        var firstDropdown = document.getElementById("firstDropdown");
        var secondDropdown = document.getElementById("secondDropdown");
        var thirdDropdown = document.getElementById("thirdDropdown");

        // Clear previous options
        secondDropdown.innerHTML = '<option disabled selected>--select semester--</option>';
        thirdDropdown.innerHTML = '<option disabled selected>--select Subject --</option>';

        // Add new options based on the selected value of the first dropdown
        if (firstDropdown.value === "option1") {
            addOptions(secondDropdown, ["Semester 1", "Semester 2","Semester 3","Semester 4","Semester 5","Semester 6"]);
        } else if (firstDropdown.value === "option2") {
              addOptions(secondDropdown, ["Semester 1", "Semester 2","Semester 3","Semester 4","Semester 5","Semester 6"]);
        } else if (firstDropdown.value === "option3") {
              addOptions(secondDropdown, ["Semester 1", "Semester 2","Semester 3","Semester 4","Semester 5","Semester 6"]);
        }
    }

    function updateThirdDropdown() {
        var secondDropdown = document.getElementById("secondDropdown");
        var thirdDropdown = document.getElementById("thirdDropdown");

        // Clear previous options
        thirdDropdown.innerHTML = "";

        // Add new options based on the selected value of the second dropdown
        if (secondDropdown.value === "Semester 1") {
            addOptions(thirdDropdown, ["subject1","subject1.1","subject1.2","subject1.3"]);
        } else if (secondDropdown.value === "Semester 2") {
            addOptions(thirdDropdown, ["subject2","subject2.1","subject2.2"]);
        } else if (secondDropdown.value === "Semester 3") {
            addOptions(thirdDropdown, ["subject3","subject3.1","subject3.2","subject3.3"]);
        } else if (secondDropdown.value === "Semester 4") {
            addOptions(thirdDropdown, ["subject4","subject4.1","subject4.2","subject4.3"]);
        } else if (secondDropdown.value === "Semester 5") {
            addOptions(thirdDropdown, ["subject5","subject5.1","subject5.2","subject5.3"]);
        } else if (secondDropdown.value === "Semester 6") {
            addOptions(thirdDropdown, ["subject6","subject6.1","subject6.2","subject6.3"]);
        }
    }

    function addOptions(selectElement, options) {
        for (var i = 0; i < options.length; i++) {
            var option = document.createElement("option");
            option.text = options[i];
            selectElement.add(option);
        }
    }

    // Initialize the second dropdown options based on the default selection in the first dropdown
    updateSecondDropdown();

     // Function to open the modal
     function openModal() {
        document.getElementById("myModal").style.display = "flex";
        
    }

     // Function to close the modal
     function closeModal() {
        document.getElementById("myModal").style.display = "none";
    }


    // Close the modal if clicked outside of it
    window.onclick = function (event) {
        var modal = document.getElementById("myModal");
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
