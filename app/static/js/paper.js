
// add paper button pressed (add paper to database) 
d3.selectAll(".btn-success").on("click", function(){
    // Create modal dialog
    var modal = d3.select("body").append("div")
        .attr("class", "modal fade")
        .attr("id", "paperFormModal")
        .attr("tabindex", "-1")
        .attr("role", "dialog")
        .attr("aria-labelledby", "paperFormModalLabel")
        .attr("aria-hidden", "true");

    var modalDialog = modal.append("div")
        .attr("class", "modal-dialog")
        .attr("role", "document");

    var modalContent = modalDialog.append("div")
        .attr("class", "modal-content");

    // Close button
    modalContent.append("button")
        .attr("type", "button")
        .attr("class", "close")
        .attr("data-dismiss", "modal")
        .attr("aria-label", "Close")
        .append("span")
        .attr("aria-hidden", "true")
        .text("×");

    // make form structure
    fieldset = d3.select("#put-add-here")
    .append("form")
    .attr("class","form-horizontal")
    .attr("action","/api/add/paper/")
    .attr("method","post")
    .append("fieldset")


    // Set form legend
    fieldset.append("legend")
        .text("Add paper to database");

    // Set form body
    var formBody = fieldset.append("div");

    d3.json("/api/request/headers/paper/",

        function(error, data){
            // get data
            paper_properties = data.properties
            paper_properties_length = paper_properties.length
            paper_title = paper_properties[0].value 

            
            // set form body
            for(i = 0; i < paper_properties_length; i++){
                form_group = formBody.append("div").attr("class","form-group")
                type = paper_properties[i].type

                element_id = "paper-"+(paper_properties[i].name).split(' ').join('-')
                value = ""
                text_label = paper_properties[i].name
                placeholder = "Insert "+text_label
                if(type == 'varchar'){
                    set_varchar_input (form_group,element_id,text_label,value,placeholder)
                }
                if(type == 'text'){
                    set_text_input(form_group,element_id,text_label,value,placeholder)
                }
                if(type == 'number'){
                    set_number_input(form_group,element_id,text_label,value,placeholder)
                }
                if(type == 'category'){
                    data = paper_properties[i].data
                    set_category_select(form_group,element_id,text_label,value,data)
                }
            }
        

        // add buttons
        form_group = fieldset.append("div").attr("class","form-group")
        // label?
        form_group.append("label")
        .attr("class","col-md-4 control-label")
        .attr("for","accept-modified-data")
        // buttons
        div_for_buttons = form_group.append("div").attr("class","col-md-8")
        put_submit_button(div_for_buttons)
        put_dismiss_button(div_for_buttons)
        // Show modal dialog
        modal.modal("show");
    });
});

// what to do if the search-paper button is pressed
var set_form_with_paper = function(paper_id){
    if(paper_id == ""){
        console.log("No match found")
        return
    }
    d3.select("#put-form-here").selectAll("table").remove()
    d3.json("/api/request/data/paper/"+paper_id+"/",
            function(error, data) {
                // get data
                paper_properties = data.properties
                paper_properties_length = paper_properties.length
                paper_title = paper_properties[0].value //paper title 
                // make table structure
                table = d3.select("#put-form-here")
                    .append("table")
                    .attr("class", "table table-bordered")
                    .append("tbody")
            
                // set table header
                table.append("tr")
                    .append("th")
                    .attr("colspan", "2")
                    .text(paper_title[0].toUpperCase() + paper_title.substring(1) + " information")
                // set table body
                for (i = 0; i < paper_properties_length; i++) {
                    row = table.append("tr")
                    type = paper_properties[i].type

                    element_id = "paper-" + paper_id + "-" + (paper_properties[i].name).split(' ').join('-')
                    value = paper_properties[i].value
                    text_label = paper_properties[i].name

                    row.append("td")
                        .text(text_label)
                    row.append("td")
                        .text(value)
                }
                // add buttons
                form_group = table.append("tr")
                // buttons
                div_for_buttons = form_group.append("td")
                    .attr("colspan", "3")
                div_for_buttons.append("button")
                    .attr("class", "btn btn-primary")
                    .text("Back")
                    .on("click", function() {
                        window.location.href = "/";
                    });

                // add modify-button
                div_for_buttons.append("button")
                    .attr("class","btn btn-warning")
                    .attr("data-toggle","modal")
                    .attr("data-target","#modify-data-modal")
                    .on("click",function(){
                        // set modal form parameter to delete row
                        row = d3.select(this).attr("value")
                        d3.select("#modify-data-modal")
                        .select("form")
                        .attr("action",'/api/edit/data/paper/'+paper_id)
                    })
                    .append("i")
                    .attr("class","fa fa-pencil-square-o fa-lg")

                

                // add delete-button
                div_for_buttons.append("button")
                    .attr("class","btn btn-danger")
                    .attr("data-toggle","modal")
                    .attr("data-target","#delete-data-modal")
                    .on("click",function(){
                        // set modal form parameter to delete row
                        row = d3.select(this).attr("value")
                        d3.select("#delete-data-modal")
                        .select("form")
                        .attr("action",'/api/delete/data/paper/'+paper_id)
                    })
                    .append("i")
                    .attr("class","fa fa-trash fa-lg")
                
            });
    }



// what to do if the modify button is pressed 
var set_form_with_paper_modify = function(paper_id){
    if(paper_id == ""){
        console.log("No match found")
        return
    }
    d3.selectAll("#modify-data-body").selectAll("form").remove()
    d3.json("/api/request/data/paper/"+paper_id+"/",
            function(error, data){
                // get data
                paper_properties = data.properties
                paper_properties_length = paper_properties.length
                paper_title = paper_properties[0].value //paper title 
                // make form structure
                fieldset = d3.select("#modify-data-body")
                .append("form")
                .attr("class","form-horizontal")
                .attr("action","/api/edit/data/paper/"+paper_id+"/")
                .attr("method","post")
                .append("fieldset")
                // set form legend
                fieldset.append("legend").text("Modify data of "+paper_title)
                // set form body
                for(i = 0; i < paper_properties_length; i++){
                    form_group = fieldset.append("div").attr("class","form-group")
                    type = paper_properties[i].type

                    element_id = "paper-"+paper_id+"-"+(paper_properties[i].name).split(' ').join('-')
                    value = paper_properties[i].value
                    placeholder = ""
                    text_label = paper_properties[i].name
                    if(type == 'varchar'){
                        set_varchar_input (form_group,element_id,text_label,value,placeholder)
                    }
                    if(type == 'text'){
                        set_text_input(form_group,element_id,text_label,value,placeholder)
                    }
                    if(type == 'number'){
                        set_number_input(form_group,element_id,text_label,value,placeholder)
                    }
                    if(type == 'category'){
                        data = paper_properties[i].data
                        set_category_select(form_group,element_id,text_label,value,data)
                    }
                }
                // add buttons
                form_group = fieldset.append("div").attr("class","form-group")
                // label?
                form_group.append("label")
                .attr("class","col-md-4 control-label")
                .attr("for","accept-modified-data")
                // buttons
                div_for_buttons = form_group.append("div").attr("class","col-md-8")
                put_submit_button(div_for_buttons)
                put_dismiss_button(div_for_buttons)
            })
}







var put_dismiss_button = function(div_for_buttons){
    div_for_buttons.append("button")
                    .attr("data-dismiss","modal")
                    .attr("class", "btn btn-danger")
                    .text("Cancel")
}

var put_submit_button = function(div_for_buttons){
    div_for_buttons.append("button")
                    .attr("id","accept-new-data")
                    .attr("type","submit")
                    .attr("name","accept-new-data")
                    .attr("class", "btn btn-success")
                    .text("Accept")

}


var set_number_input = function(form_group,id,text_label,value,placeholder){
    form_group.append("label")
        .attr("class","col-md-2 control-label")
        .attr("for",id)
        .text(text_label)
    input_element = form_group.append("div")
        .attr("class","col-xs-3")
        .append("input")
        .attr("id",id)
        .attr("name",id)
        .attr("type","number")
        .attr("autocomplete","off")
        .attr("class","form-control input-md")
    if(placeholder == ""){
        input_element.attr("value",value)
    }
    if(value == ""){
        input_element.attr("placeholder",placeholder)
    }

}

var set_varchar_input = function(form_group,id,text_label,value,placeholder){
    form_group.append("label")
                .attr("class","col-md-2 control-label")
                .attr("for",id)
                .text(text_label)
    input_element = form_group.append("div")
                .attr("class","col-md-8")
                .append("input")
                .attr("id",id)
                .attr("name",id)
                .attr("type","text")
                .attr("autocomplete","off")
                .attr("class","form-control input-md")

    if(placeholder == ""){
        input_element.attr("value",value)
    }
    if(value == ""){
        input_element.attr("placeholder",placeholder)
    }

}

var set_text_input = function(form_group,id,text_label,value,placeholder){
                    form_group.append("label")
                    .attr("class","col-md-2 control-label")
                    .attr("for",id)
                    .text(text_label)
    input_element = form_group.append("div")
                    .attr("class","col-md-8")
                    .append("textarea")
                    .attr("id",id)
                    .attr("name",id)
                    .attr("autocomplete","off")
                    .attr("class","form-control input-md")
    if(placeholder == ""){
        input_element.text(value)
    }
    if(value == ""){
        input_element.attr("placeholder",placeholder)
    }

}

var set_category_select = function(form_group,id,text_label,value,data){
    // add label to dropdown
    form_group.append("label")
    .attr("class","col-md-2 control-label")
    .attr("for",id)
    .text(text_label)
    // add dropdown
    form_group.append("div")
    .attr("class","col-md-8")
    .append("select")
    .attr("id",id)
    .attr("name",id)
    .attr("class","form-control")
    .attr("multiple","multiple")
    put_options_here = d3.select("#"+id)
    // get length of subcategories
    data_length = data.length
    // put options on dropdown
    for(var j = 0; j < data_length; j++){
        option = put_options_here
        .append("option")
        .attr("value",data[j].id)
        .text(data[j].name)
        option
        .property("selected",function(d,i){
            for (var i=0; i< value.length; i++){
                if (d3.select(this).text() == value[i]){
                    return true
                }
            }
        })
    }


}
