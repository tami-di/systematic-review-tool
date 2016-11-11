// what to do if the search-paper button is pressed
d3.selectAll(".btn-success").on("click", function(){
    d3.select("#put-form-here").selectAll("form").remove()
    d3.json("/api/request_data/paper/",
            function(error, data){
            // get data
            paper_properties = data.properties
            paper_properties_length = paper_properties.length
            paper_title = paper_properties[0].value
            // make form structure
            fieldset = d3.select("#put-form-here")
            .append("form")
            .attr("class","form-horizontal")
            .attr("action","/api/add_paper/")
            .attr("method","post")
            .append("fieldset")
            // set form legend
            fieldset.append("legend").text("Add paper to database")
            // set form body
            for(i = 0; i < paper_properties_length; i++){
                form_group = fieldset.append("div").attr("class","form-group")
                type = paper_properties[i].type

                element_id = "paper-"+(paper_properties[i].name).replace(" ","-")
                value = ""
                text_label = paper_properties[i].name
                placeholder = "Instert "+text_label
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

})

// what to do if the search-paper button is pressed (any search really)
var set_form_with_paper = function(paper_id){
    if(paper_id == ""){
        console.log("No hay paper")
        return
    }
    d3.select("#put-form-here").selectAll("form").remove()
    d3.json("/api/request_data/paper/"+paper_id+"/",
            function(error, data){
                // get data
                paper_properties = data.properties
                paper_properties_length = paper_properties.length
                paper_title = paper_properties[0].value
                // make form structure
                fieldset = d3.select("#put-form-here")
                .append("form")
                .attr("class","form-horizontal")
                .attr("action","/api/edit_paper/"+paper_id+"/")
                .attr("method","post")
                .append("fieldset")
                // set form legend
                fieldset.append("legend").text("Modificar datos de "+paper_title)
                // set form body
                for(i = 0; i < paper_properties_length; i++){
                    form_group = fieldset.append("div").attr("class","form-group")
                    type = paper_properties[i].type

                    element_id = "paper-"+paper_id+"-"+(paper_properties[i].name).replace(" ","-")
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
                    .text("cancelar")
}

var put_submit_button = function(div_for_buttons){
    div_for_buttons.append("button")
                    .attr("id","accept-new-data")
                    .attr("type","submit")
                    .attr("name","accept-new-data")
                    .attr("class", "btn btn-success")
                    .text("Aceptar")

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
        //if(data[j].name in value){
        //    option.property("selected")
        //}
    }
    /*sel = ["a", "c"]
    d3.selectAll("option")
    .property("selected", function(d,i){
        for (var i=0; i< sel.length; i++){
            if (d3.select(this).attr("id") == value[i]){
                return true
            }
        }
    })*/


}
