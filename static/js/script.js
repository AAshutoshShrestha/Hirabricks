 //Query All input fields
 var form_label = document.getElementsByTagName("label");
 var form_fields = document.getElementsByTagName("input");
 var form_textarea = document.getElementsByTagName("textarea");
 var form_select = document.getElementsByTagName("select");
 var form_option = document.getElementsByTagName("option");
 var form_helptxt = document.getElementsByClassName("helptext");
 var form_errorlist = document.getElementsByClassName("errorlist");
 
 for (var field in form_label) {
   form_label[field].className +=
     "mt-4 block mb-2 text-sm font-medium text-gray-900 dark:text-white";
 }
 
 for (var field in form_fields) {
   form_fields[field].className +=
     "block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-red-600 focus:ring-red-600 sm:text-sm dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500";
 }
 for (var field in form_textarea) {
   form_textarea[field].className +=
     "block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-red-500 focus:ring-red-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-red-500 dark:focus:ring-red-500";
 }

 for (var field in form_select) {
   form_select[field].className +=
     "block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-red-500 focus:ring-red-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 dark:focus:border-red-500 dark:focus:ring-red-500 cursor-pointer";
 }

 for (var field in form_option) {
   form_option[field].className +=
     "ml-2 text-sm font-medium text-gray-900 text-left";
 }

 for (var field in form_helptxt) {
   form_helptxt[field].className +=
     " hidden text-sm font-light text-gray-500 dark:text-gray-400";
 }
 
 for (var field in form_errorlist) {
  form_errorlist[field].className +=
     " hidden";
 }


function clearSearch() {
  // Clear the search input field
  document.getElementById('search').value = '';

  // Remove the search query parameter from the URL and reload the page
  const urlWithoutSearch = window.location.href.split('?')[0]; // Get the URL without query parameters
  window.location.href = urlWithoutSearch; // Reload the page without the search query parameter
}