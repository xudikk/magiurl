var countdown = 10; // Initial countdown time in seconds

        function closePopup() {
            document.getElementById('popupContainer').style.display = 'none';
        }

        function handleContinue() {
            // Add your logic for handling the "Continue as Google Account" button click
            console.log('Continue as Google Account clicked');
            // You can close the popup here if needed
            closePopup();
        }

        // Show the popup when the page loads
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('popupContainer').style.display = 'block';

            // Automatically close the popup after 60 seconds
            var countdownInterval = setInterval(function() {
                countdown--;
                document.getElementById('timerDisplay').innerText = 'Closing in ' + countdown + 's';

                if (countdown <= 0) {
                    closePopup();
                    clearInterval(countdownInterval); // Stop the countdown when the popup is closed
                }
            }, 1000); // Update the countdown every 1000 milliseconds (1 second)
        });