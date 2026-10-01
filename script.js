console.log("JavaScript خدام");

const menuButton = document.getElementById("menuBtn");

const menuSection = document.getElementById("menu");

menuButton.addEventListener("click", function () {

    menuSection.scrollIntoView({
        behavior: "smooth"
    });

});


const bookingButton = document.getElementById("bookingBtn");

const bookingBox = document.getElementById("bookingBox");

bookingButton.addEventListener("click", function () {

    bookingBox.innerHTML = `
        <h3>حجز طاولة</h3>

        <label>الاسم</label>
        <input id="nameInput" type="text" placeholder="أدخل اسمك">

        <label>عدد الأشخاص</label>
        <input id="peopleInput" type="number" placeholder="عدد الأشخاص">

        <label>تاريخ الحجز</label>
        <input id="dateInput" type="date">

        <label>وقت الحجز</label>
        <input id="timeInput" type="time">

        <label>رقم الهاتف</label>
        <input id="phoneInput" type="tel" placeholder="أدخل رقم هاتفك">

        <label>ملاحظات</label>
        <textarea id="notesInput" placeholder="هل لديك أي ملاحظات؟"></textarea>

        <button id="confirmBookingBtn">تأكيد الحجز</button>
    `;

    const confirmBookingButton =
    document.getElementById("confirmBookingBtn");

confirmBookingButton.addEventListener("click", function () {

    const name =
        document.getElementById("nameInput").value;

    const people =
        document.getElementById("peopleInput").value;

    const date =
        document.getElementById("dateInput").value;

    const time =
        document.getElementById("timeInput").value;

    const phone =
        document.getElementById("phoneInput").value;

    const notes =
        document.getElementById("notesInput").value;


    
if (!name) {
    alert("المرجو إدخال الاسم");
    return;
}


if (!people || people < 1) {
    alert("المرجو إدخال عدد صحيح من الأشخاص");
    return;
}


if (!date) {
    alert("المرجو اختيار تاريخ الحجز");
    return;
}


if (!time) {
    alert("المرجو اختيار وقت الحجز");
    return;
}


if (!phone) {
    alert("المرجو إدخال رقم الهاتف");
    return;
}


if (!/^0[5-7][0-9]{8}$/.test(phone)) {
    alert("المرجو إدخال رقم هاتف مغربي صحيح");
    return;
}


bookingBox.innerHTML = ` <div class="success-message"> <h3>✅ تم تأكيد الحجز بنجاح</h3> <p>مرحبا ${name} 👋</p> <p>عدد الأشخاص: ${people}</p> <p>التاريخ: ${date}</p> <p>الوقت: ${time}</p> <p>رقم الهاتف: ${phone}</p> <p>ملاحظات: ${notes || "لا توجد ملاحظات"}</p> <p>نتمنى لك تجربة مميزة في مطعم الذوق المغربي 🌿</p> </div> `; }); });


