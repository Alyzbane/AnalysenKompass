function addFormToFormset(buttonId, formsetId, totalFormsId) {
    document.getElementById(buttonId).addEventListener('click', function() {
        var formIdx = document.getElementById(totalFormsId).value;
        var newFormHtml = document.getElementById('empty-form').innerHTML.replace(/__prefix__/g, formIdx);
        document.getElementById(formsetId).innerHTML += newFormHtml;
        document.getElementById(totalFormsId).value = parseInt(formIdx) + 1;
    });
}
