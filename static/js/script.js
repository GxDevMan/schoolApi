// const body = document.querySelector("body"),
//       modeToggle = body.querySelector(".mode-toggle");
//       sidebar = body.querySelector("nav");
//       sidebarToggle = body.querySelector(".sidebar-toggle");

// let getMode = localStorage.getItem("mode");
// if(getMode && getMode ==="dark"){
//     body.classList.toggle("dark");
// }

// let getStatus = localStorage.getItem("status");
// if(getStatus && getStatus ==="close"){
//     sidebar.classList.toggle("close");
// }

// modeToggle.addEventListener("click", () =>{
//     body.classList.toggle("dark");
//     if(body.classList.contains("dark")){
//         localStorage.setItem("mode", "dark");
//     }else{
//         localStorage.setItem("mode", "light");
//     }
// });

// sidebarToggle.addEventListener("click", () => {
//     sidebar.classList.toggle("close");
//     if(sidebar.classList.contains("close")){
//         localStorage.setItem("status", "close");
//     }else{
//         localStorage.setItem("status", "open");
//     }
// })



// Select All

// function checkall(formname, checkname, thestate) {
//     var el_collection = eval(
//       "document.forms." + formname + "." + checkname
//     );
//     for (c = 0; c < el_collection.length; c++)
//       el_collection[c].checked = thestate;
//   }




//overlays

function openForm() {
    document.getElementById("myOverlay").style.display ="block";
}
function closeForm() {
    document.getElementById("myOverlay").style.display ="none";
}

function openFormClear() {
    document.getElementById("clearOverlay").style.display ="block";
}

function openFormUpdateHistory() {
    document.getElementById("updateHistoryOverlay").style.display ="block";
}

function openFormDeleteHistory() {
    document.getElementById("deleteHistoryOverlay").style.display ="block";
}

function openFormGenerateReport() {
    document.getElementById("generateReportOverlay").style.display ="block";
}

function openFormMarkItems() {
    document.getElementById("markItemsOverlay").style.display ="block";
}

function openFormReturnItems() {
    document.getElementById("returnItemsOverlay").style.display ="block";
}

function openFormDeleteItems() {
    document.getElementById("deleteItemsOverlay").style.display ="block";
}

function openFormUpdateItems() {
    document.getElementById("updateItemsOverlay").style.display ="block";
}

function openFormAddItems() {
    document.getElementById("addItemsOverlay").style.display ="block";
}

function openFormAddCategory() {
    document.getElementById("addCategoryOverlay").style.display ="block";
}

function openFormDeleteCategory() {
    document.getElementById("deleteCategoryOverlay").style.display ="block";
}

function openFormDeleteUsers() {
    document.getElementById("deleteUsersOverlay").style.display ="block";
}

function openFormUpdateUsers() {
    document.getElementById("updateUsersOverlay").style.display ="block";
}

function openFormResetPassword() {
    document.getElementById("resetPasswordOverlay").style.display ="block";
}

function openFormCancel() {
    document.getElementById("cancelOverlay").style.display ="block";
}

function openFormUserReserve() {
    document.getElementById("userReserveOverlay").style.display ="block";
}

function openFormGenerateInvoice() {
    document.getElementById("generateInvoiceOverlay").style.display ="block";
}

function openFormReserve() {
    document.getElementById("reserveOverlay").style.display ="block";
}

function openFormBorrow() {
    document.getElementById("borrowOverlay").style.display ="block";
}

function openFormReservation() {
    document.getElementById("reservationOverlay").style.display ="block";
}

function openFormRemove() {
    document.getElementById("removeOverlay").style.display ="block";
}

function openFormGenerateQR() {
    document.getElementById("generateQROverlay").style.display ="block";
}

function openFormBackpack() {
    document.getElementById("backpackOverlay").style.display ="block";
}

function openFormUserBackpack() {
    document.getElementById("userBackpackOverlay").style.display ="block";
}

function openFormScanQR() {
    document.getElementById("scanQROverlay").style.display ="block";
}

function openFormReservationScanQR() {
    document.getElementById("reservationScanQROverlay").style.display ="block";
}



