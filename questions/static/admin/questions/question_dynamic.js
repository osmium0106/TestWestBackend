(function($) {
    $(document).ready(function() {
        function toggleOptions() {
            var qtype = $('#id_question_type').val();
            var showOptions = (qtype === 'mcq' || qtype === 'msq');
            var optionFields = ['option_a', 'option_b', 'option_c', 'option_d'];
            optionFields.forEach(function(opt) {
                var row = $('#id_' + opt).closest('.form-row, .field-' + opt);
                if (showOptions) {
                    row.show();
                } else {
                    row.hide();
                }
            });
        }
        toggleOptions();
        $('#id_question_type').change(toggleOptions);
    });
})(django.jQuery);
