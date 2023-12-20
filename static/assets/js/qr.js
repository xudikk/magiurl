let formContainer = document.getElementById("qrcode");
let qrcodeInstance = null;
$('#shortenedQrContainer').hide();

function showQrForm() {
    hideAllForms();
    formContainer.style.display = "block";
    document.getElementById("qrForm").style.display = "block";
}

function showUrlForm() {
    hideAllForms();
    document.getElementById('urlForm').style.display = 'block';
}

function hideAllForms() {
    formContainer.style.display = "none";
    document.getElementById("qrForm").style.display = "none";
    document.getElementById('urlForm').style.display = 'none';
}

function showForm() {
    formContainer.style.display = "block";
    formContainer.style.transform = "scale(1)";
    document.getElementById("overlay").style.display = "block";
}

function hideForm() {
    formContainer.style.transform = "scale(0)";
    setTimeout(() => {
        document.getElementById("overlay").style.display = "none";
    }, 300);
}

function generateAndShowQRCode() {
    const inputField = document.getElementById("qrInput");
    const longUrl = inputField.value.trim();


    if (longUrl) {
        $.ajax({
            type: 'POST',
            url: 'qr_short/',
            data: { 'qrInput': longUrl },
            headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data) {
                const completeUrl = "http://209.38.220.77/" + data.short_url;
                $('#shortenedQr').html(completeUrl);
                generateQRCode(completeUrl);
                $('#shortenedQrContainer').hide().fadeIn(300);
                showForm();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    } else {
        alert("Please enter a long URL for the QR code.");
    }
}

function generateQRCode(shortUrl) {
    if (!qrcodeInstance) {
        qrcodeInstance = new QRCode(document.querySelector(".qr-code"), {
            width: 160,
            height: 150
        });
    }

    qrcodeInstance.clear();
    qrcodeInstance.makeCode(shortUrl);
}

function downloadQRCode() {
    let downloadLink = document.createElement("a");
    downloadLink.setAttribute("download", "qr_code.png");

    let qrCodeImg = document.querySelector(".qr-code img");
    let qrCodeCanvas = document.querySelector("canvas");

    if (qrCodeImg && qrCodeImg.getAttribute("src") !== null) {
        downloadLink.setAttribute("href", qrCodeImg.getAttribute("src"));
    } else if (qrCodeCanvas) {
        downloadLink.setAttribute("href", qrCodeCanvas.toDataURL());
    } else {
        console.error("No QR code found to download.");
        return;
    }

    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

function myQrFunction() {
    var copyText = document.getElementById("shortenedQr").innerText;
    var tempTextArea = document.createElement("textarea");
    tempTextArea.value = copyText;

    document.body.appendChild(tempTextArea);

    tempTextArea.select();

    document.execCommand('copy');

    document.body.removeChild(tempTextArea);
    $("#copyButtonQr").text("Copied");

    setTimeout(function() {
        $("#copyButtonQr").text("Copy");
    }, 1000);
}