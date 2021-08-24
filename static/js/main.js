$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                
                $('#solution-div').text("SOLUTION:\n");
                if(data === 'Sigatoka'){
                     $('#solution-div').append("Orchard grade mineral oil can be sprayed on the banana every three weeks for a total of 12 applications to control Sigatoka. \nCommercial growers also use aerial spraying and systemic fungicide application to control the disease. \nSome banana cultivars also show some resistance to Sigatoka.");
                     //$('#solution-div').attr('style','color:red;');
                }else if(data === 'Pestalotiopsis'){
                     $('#solution-div').append("Pestalotiopsis is a genus of ascomycete fungi.\nPestalotiopsis species are known as plant pathogens.\nChemical treatments with Topsin 70 WDG and Topsin 500 SC. Prepare a solution of 0.05 – 0.1% (5 or 10 g per 10 litres of water) and spray each plant with 0.5 l (of the solution); Blight, produced by Phythophtora infestans.");
                     //$('#solution-div').attr('style','color:green;');
                }else if(data === 'Cordana'){
                     $('#solution-div').append("Spray 0.25% Kavach or 0.25% Indofil M-45 or 0.1% Tilt at 15 days interval");
                     //$('#solution-div').attr('style','color:yellow;');
                }else if(data === 'Healthy'){
                     $('#solution-div').append("Bananas need a rich but well-drained soil. Soil similar to that in Hawaii – with some small rocks and lava sand – promotes the excellent drainage these plants require. Well-rotted manure, leaf mold or organic compost add humus and the important nutrients. Commercial cactus mix plus humus or compost is a good choice, or add 2/3 of this mix to 1/3 native soil. A banana likes plenty of water and will not tolerate drought. However, wet soil increases the risk of root rot. In summer, a banana plant – especially if outside or in a container – may need water at least every other day. In winter, when plants are semi-dormant, you may only need to water once a week or less. Check the soil daily – it should be evenly moist.");
                     //$('#solution-div').attr('style','color:darkgrey;');
                }

                
                console.log('Success!');
            },
        });
    });

});
