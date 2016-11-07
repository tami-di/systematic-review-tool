// what to do if the add-data-to-category button is pressed
d3.selectAll("#categorias").selectAll(".btn-success").on("click", function(){
    // get category id
    cat_name = d3.select(this).attr("value")
    parent = this.parentNode
    cat_id = d3.select(parent).select(".btn-grey").attr("value")
    d3.json("/api/category/"+ cat_id + "/subcategories",
            function(error, data){
                if (error){
                    console.log(error);
                    return
                }
            // save subcategories into variable
            subcategories = data.subcategories
            // get length of subcategories
            length = subcategories.length
            title_message = d3.select("#add-data-message")
            title_message.text("Añadir dato a " + cat_name.trim())
            form_body = d3.select("#add-data-body")
            // set action to form
            form = d3.select(form_body.node().parentNode)
            form.attr("action","/api/add_data/category/" + cat_id)
            // remove last elements of the form
            d3.select("#add-data-body").selectAll(".form-group").remove()
            for(var i = 0; i < length; i++){
                form_group = form_body.append("div").attr("class","form-group")
                type = subcategories[i].type
                subcat_id = subcategories[i].id
                element_id = "sub-"+subcategories[i].id+"-cat-"+cat_id
                text_label = subcategories[i].name
                value = ""
                if(type == 'varchar'){
                    placeholder = "Inserte "+subcategories[i].name
                    set_varchar_input (form_group,element_id,text_label,value,placeholder)
                }
                if(type == 'text'){
                    placeholder = "Inserte "+subcategories[i].name
                    set_text_input(form_group,element_id,text_label,value,placeholder)
                }
                if(type == 'number'){
                    placeholder = "-"
                    set_number_input(form_group,element_id,text_label,value,placeholder)
                }
                if(type == 'subcat'){
                    value = ""
                    set_subcategory_select(form_group,element_id,text_label,value,cat_id,subcat_id)
                }
            }
            // add buttons
            form_group = form_body.append("div").attr("class","form-group")
            // label?
            form_group.append("label")
            .attr("class","col-md-4 control-label")
            .attr("for","accept-new-data")
            // buttons
            div_for_buttons = form_group.append("div").attr("class","col-md-8")
            put_submit_button(div_for_buttons)
            put_dismiss_button(div_for_buttons)

            })
})
// what to do if the category button is pressed
d3.selectAll("#categorias").selectAll(".btn-grey").on("click", function(){
    // get category id
    cat_id = d3.select(this).attr("value")
    // get category name
    parent = this.parentNode
    cat_name = d3.select(parent).select(".btn-success").attr("value")
    // set clicked item active, set rest unactive
    set_active("#categorias",this)
    // remove last subcategories shown
    d3.select("#subcategorias").selectAll("div").remove()
    d3.select("#subcategorias").selectAll("button").remove()

    d3.select("#subcategorias")
                .attr("class","panel-group col-md-3")
                .append("div")
                .attr("class","row")
                .append("div")
                .attr("class","col-md-12")
                .append("h4")
                .attr("class","text-center")
                .text("Subcategorias de la Categoria " + cat_id)

    // get subcategories of current category
    d3.json("/api/category/"+ cat_id + "/subcategories",
    function(error, data){
        if (error){
            console.log(error);
            return
        }
        // save subcategories into variable
        subcategories = data.subcategories
        // get length of subcategories
        length = subcategories.length
        // set a button for each subcategory
        for(var i = 0; i < length; i++){
            if(subcategories[i].type == 'subcat'){
                subcategory_buttons_container =
                d3.select("#subcategorias")
                .append("div")
                .attr("class","row")
                .append("div")
                .attr("class","col-md-12")
                // set subcategory button
                subcategory_buttons_container.append("button")
                .attr("class","btn btn-grey btn-ctnr-data")
                .attr("id","subcat"+subcategories[i].id)
                .attr("value",cat_id + "." + subcategories[i].id)
                .text(subcategories[i].name)
                // set see-all-data from subcategory button
                subcategory_buttons_container.append("button")
                .attr("type","button")
                .attr("id","see-all-data-of-subcat-" + cat_id + "." + subcategories[i].id)
                .attr("name","see-all-data-of-subcat-" + cat_id + "." + subcategories[i].id)
                .attr("class","btn btn-info")
                .attr("value",subcategories[i].name)
                .append("i")
                .attr("class","fa fa-search-plus fa-lg")
                // set add data to subcategory
                subcategory_buttons_container.append("button")
                .attr("type","button")
                .attr("id","add-data-to-subcat-" + cat_id + "." + subcategories[i].id)
                .attr("name","add-data-to-subcat-" + cat_id + "." + subcategories[i].id)
                .attr("data-toggle","modal")
                .attr("data-target","#add-data-modal")
                .attr("class","btn btn-success")
                .attr("value",subcategories[i].name)
                .append("i")
                .attr("class","fa fa-plus-circle fa-lg")
            }
        }
        // what to do if the see-all-data-of-category button is pressed
        d3.selectAll("#subcategorias").selectAll(".btn-info").on("click", function(){
            parent = this.parentNode
            id = (d3.select(parent).select(".btn-grey").attr("value")).split(".")
            cat_id = id[0]
            subcat_id = id[1]
            d3.select("#table-placer").selectAll("table").remove()
            the_table = d3.select("#table-placer")
            .append("table")
            .attr("class","table table-bordered table-striped table-hover table-responsive")
            d3.json("/api/request_data/category/"+ cat_id +"/subcategory/"+subcat_id,
                function(error, data){
                    if (error){
                        console.log(error);
                        return
                    }
                column_headers = data.column_headers
                column_headers_length = column_headers.length
                header_row = the_table.append("thead").append("tr")

                for(var i = 0; i < column_headers_length; i++){
                    header_row.append("td")
                    .text(column_headers[i]+" "+cat_id)
                }
                // append row for buttons
                header_row.append("td")
                .text("Editar/Eliminar")

                column_data = data.column_data
                column_data_length = column_data.length
                table_body = the_table.append("tbody")
                for(var j = 0; j < column_data_length; j++){
                    body_row = table_body.append("tr")
                    for(var k = 0; k < column_headers_length; k++){
                        body_row.append("td")
                        .text(column_data[j][column_headers[k]])
                    }
                }
        })

        })
        // what to do if the add-data-to-subcategory button is pressed
        d3.selectAll("#subcategorias").selectAll(".btn-success").on("click", function(){
            // get category id
            subcat_name = d3.select(this).attr("value")
            parent = this.parentNode
            id = (d3.select(parent).select(".btn-grey").attr("value")).split(".")
            cat_id = id[0]
            subcat_id = id[1]
            d3.json("/api/category/"+ cat_id + "/subcategories",
                    function(error, data){
                        if (error){
                            console.log(error);
                            return
                        }
                    // save subcategories into variable
                    subcategories = data.subcategories
                    // get length of subcategories
                    length = subcategories.length
                    title_message = d3.select("#add-data-message")
                    title_message.text("Añadir dato a " + subcat_name.trim())
                    form_body = d3.select("#add-data-body")
                    // set action to form
                    form = d3.select(form_body.node().parentNode)
                    form.attr("action","/api/add_data/category/" + cat_id + "/subcategory/" + subcat_id)
                    // remove last elements of the form
                    d3.select("#add-data-body").selectAll(".form-group").remove()
                    for(var i = 0; i < length; i++){

                        type = subcategories[i].type
                        if(type == 'subcat'){
                            properties_of_subcategory = subcategories[i].properties
                            properties_types = subcategories[i].properties_type
                            properties_of_subcategory_length = properties_of_subcategory.length
                            for(var j = 0; j < properties_of_subcategory_length; j++){
                                form_group = form_body.append("div").attr("class","form-group")
                                name = properties_of_subcategory[j]
                                property_type = properties_types[name]
                                element_id = "sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name
                                text_label = name
                                value = ""
                                if(property_type == 'varchar'){
                                    placeholder = "Inserte "+name
                                    set_varchar_input(form_group,element_id,text_label,value,placeholder)
                                }
                                if(property_type == 'text'){
                                    placeholder = "Inserte "+name
                                    set_text_input(form_group,element_id,text_label,value,placeholder)
                                }
                                if(property_type == 'number'){
                                    placeholder = "-"
                                    set_number_input(form_group,element_id,text_label,value,placeholder)
                                }

                            }
                        }

                    }
                    // add buttons
                    form_group = form_body.append("div").attr("class","form-group")
                    // label?
                    form_group.append("label")
                    .attr("class","col-md-4 control-label")
                    .attr("for","accept-new-data")
                    // buttons
                    div_for_buttons = form_group.append("div").attr("class","col-md-8")
                    put_submit_button(div_for_buttons)
                    put_dismiss_button(div_for_buttons)

                    })
        })
        // what to do if the see-all-data-of-subcategory button is pressed
        d3.selectAll("#subcategorias").selectAll(".btn-info").on("click", function(){
            // get category id
            subcat_name = d3.select(this).attr("value")
            parent = this.parentNode
            id = (d3.select(parent).select(".btn-grey").attr("value")).split(".")
            cat_id = id[0]
            subcat_id = id[1]
            d3.select("#table-placer").selectAll("table").remove()
            the_table = d3.select("#table-placer")
            .append("table")
            .attr("class","table table-bordered table-striped table-hover table-responsive")

            d3.json('/api/request_data/category/'+cat_id+'/subcategory/'+subcat_id,
                function(error, data){
                    if (error){
                        console.log(error);
                        return
                    }
                column_headers = data.column_headers
                column_headers_length = column_headers.length
                header_row = the_table.append("thead").append("tr")
                for(var i = 0; i < column_headers_length; i++){
                    header_row.append("td")
                    .text(column_headers[i].name+" "+cat_id)
                }
                // append row for buttons
                header_row.append("td")

                column_data = data.column_data
                column_data_length = column_data.length
                table_body = the_table.append("tbody")
                for(var j = 0; j < column_data_length; j++){
                    body_row = table_body.append("tr")
                                .attr("id","row-"+j)
                    for(var k = 0; k < column_headers_length; k++){
                        body_row.append("td")
                        .attr("id","cell-"+j+"-"+k)
                        .text(column_data[j][column_headers[k].name])
                    }
                    last_column = body_row.append("td")
                    // add edit-row-button
                    last_column.append("button")
                    .attr("class","btn btn-warning")
                    .attr("value",j)
                    .attr("data-toggle","modal")
                    .attr("data-target","#modify-data-modal")
                    .on("click",function(){
                        row = d3.select(this).attr("value")
                        // save subcategories into variable
                        subcategories = column_headers
                        // get length of subcategories
                        length = subcategories.length
                        title_message = d3.select("#modify-data-message")
                        title_message.text("Modificar dato de " + cat_name.trim())
                        form_body = d3.select("#modify-data-body")
                        // set action to form
                        form = d3.select(form_body.node().parentNode)
                        form.attr("action",'/api/edit_data/'+cat_id+'/category/'+subcat_id+'/subcategory/'+row+'/row')
                        // remove last elements of the form
                        d3.select("#modify-data-body").selectAll(".form-group").remove()
                        for(var i = 0; i < length; i++){
                            form_group = form_body.append("div").attr("class","form-group")
                            type = subcategories[i].type
                            id = subcategories[i].id
                            name = subcategories[i].name
                            // set parameters for each type of input
                            value = column_data[row][column_headers[i].name]
                            placeholder = ""
                            element_id = "sub-"+subcat_id+"-cat-"+cat_id+"-"+name
                            text_label = subcategories[i].name

                            if(type == 'varchar'){
                                set_varchar_input(form_group,element_id,text_label,value,placeholder)
                            }
                            if(type == 'text'){
                                set_text_input(form_group,element_id,text_label,value,placeholder)
                            }
                            if(type == 'number'){
                                set_number_input(form_group,element_id,text_label,value,placeholder)
                            }

                        }
                        // add buttons
                        form_group = form_body.append("div").attr("class","form-group")
                        // label?
                        form_group.append("label")
                        .attr("class","col-md-4 control-label")
                        .attr("for","accept-modified-data")
                        // buttons
                        div_for_buttons = form_group.append("div").attr("class","col-md-8")
                        put_submit_button(div_for_buttons)
                        put_dismiss_button(div_for_buttons)

                    })
                    .append("i")
                    .attr("class","fa fa-pencil-square-o fa-lg")
                    // add delete-row-button
                    last_column.append("button")
                    .attr("class","btn btn-danger")
                    .attr("id","btn-delete-row-"+j)
                    .attr("value",j)
                    .attr("data-toggle","modal")
                    .attr("data-target","#delete-data-modal")
                    .on("click",function(){
                        // set modal form parameter to delete row
                        row = d3.select(this).attr("value")
                        d3.select("#delete-data-modal")
                        .select("form")
                        .attr("action",'/api/delete_data/category/'+cat_id+'/subcategory/'+subcat_id+'/row/'+row)

                    })
                    .append("i")
                    .attr("class","fa fa-trash fa-lg")


                }
            })
        })
    })



})

// what to do if the see-all-data-of-category button is pressed
d3.selectAll("#categorias").selectAll(".btn-info").on("click", function(){
        cat_name = d3.select(this).attr("value")
        parent = this.parentNode
        cat_id = d3.select(parent).select(".btn-grey").attr("value")
        d3.select("#table-placer").selectAll("table").remove()
        the_table = d3.select("#table-placer")
        .append("table")
        .attr("class","table table-bordered table-striped table-hover table-responsive")

        d3.json("/api/request_data/category/"+ cat_id ,
            function(error, data){
                if (error){
                    console.log(error);
                    return
                }
            column_headers = data.column_headers
            column_headers_length = column_headers.length
            header_row = the_table.append("thead").append("tr")
            for(var i = 0; i < column_headers_length; i++){
                header_row.append("td")
                .text(column_headers[i].name+" "+cat_id)
            }
            // append row for buttons
            header_row.append("td")

            column_data = data.column_data
            column_data_length = column_data.length
            table_body = the_table.append("tbody")
            for(var j = 0; j < column_data_length; j++){
                body_row = table_body.append("tr")
                            .attr("id","row-"+j)
                for(var k = 0; k < column_headers_length; k++){
                    body_row.append("td")
                    .attr("id","cell-"+j+"-"+k)
                    .text(column_data[j][column_headers[k].name])
                }
                last_column = body_row.append("td")
                // add edit-row-button
                last_column.append("button")
                .attr("class","btn btn-warning")
                .attr("value",j)
                .attr("data-toggle","modal")
                .attr("data-target","#modify-data-modal")
                .on("click",function(){
                    row = d3.select(this).attr("value")
                    // save subcategories into variable
                    subcategories = column_headers
                    // get length of subcategories
                    length = subcategories.length
                    title_message = d3.select("#modify-data-message")
                    title_message.text("Modificar dato de " + cat_name.trim())
                    form_body = d3.select("#modify-data-body")
                    // set action to form
                    form = d3.select(form_body.node().parentNode)
                    form.attr("action",'/api/edit_data/'+cat_id+'/category/'+row+'/row')
                    // remove last elements of the form
                    d3.select("#modify-data-body").selectAll(".form-group").remove()
                    for(var i = 0; i < length; i++){
                        form_group = form_body.append("div").attr("class","form-group")
                        type = subcategories[i].type
                        subcat_id = subcategories[i].id
                        // set parameters for each type of input
                        value = column_data[row][column_headers[i].name]
                        placeholder = ""
                        element_id = "sub-"+subcategories[i].id+"-cat-"+cat_id
                        text_label = subcategories[i].name
                        if(type == 'varchar'){
                            set_varchar_input(form_group,element_id,text_label,value,placeholder)
                        }
                        if(type == 'text'){
                            set_text_input(form_group,element_id,text_label,value,placeholder)
                        }
                        if(type == 'number'){
                            set_number_input(form_group,element_id,text_label,value,placeholder)
                        }
                        if(type == 'subcat'){
                            set_subcategory_select(form_group,element_id,text_label,value,cat_id,subcat_id)
                        }
                    }
                    // add buttons
                    form_group = form_body.append("div").attr("class","form-group")
                    // label?
                    form_group.append("label")
                    .attr("class","col-md-4 control-label")
                    .attr("for","accept-modified-data")
                    // buttons
                    div_for_buttons = form_group.append("div").attr("class","col-md-8")
                    put_submit_button(div_for_buttons)
                    put_dismiss_button(div_for_buttons)

                })
                .append("i")
                .attr("class","fa fa-pencil-square-o fa-lg")
                // add delete-row-button
                    last_column.append("button")
                    .attr("class","btn btn-danger")
                    .attr("id","btn-delete-row-"+j)
                    .attr("value",j)
                    .attr("data-toggle","modal")
                    .attr("data-target","#delete-data-modal")
                    .on("click",function(){
                        // set modal form parameter to delete row
                        row = d3.select(this).attr("value")
                        d3.select("#delete-data-modal")
                        .select("form")
                        .attr("action",'/api/delete_data/category/'+cat_id+'/row/'+row)

                    })
                    .append("i")
                    .attr("class","fa fa-trash fa-lg")

            }

        })



})

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

var set_active = function(id, object){
                    d3.selectAll(id).selectAll("button").
                    classed("active", false)
                    d3.select(object).
                    classed("active", true)
                }

var set_number_input = function(form_group,id,text_label,value,placeholder){
    form_group.append("label")
        .attr("class","col-md-4 control-label")
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
                .attr("class","col-md-4 control-label")
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
                    .attr("class","col-md-4 control-label")
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


var set_subcategory_select = function(form_group,id,text_label,value,cat_id,subcat_id){
    // add label to dropdown
    form_group.append("label")
    .attr("class","col-md-4 control-label")
    .attr("for",id)
    .text(text_label)
    // add dropdown
    form_group.append("div")
    .attr("class","col-md-8")
    .append("select")
    .attr("id",id)
    .attr("name",id)
    .attr("class","form-control")
    put_options_here = d3.select("#"+id)
    d3.json("/api/category/"+ cat_id + "/subcategory_data/"+subcat_id,
    function(error, data){
        if (error){
            console.log(error);
            return
        }

        // save subcategories into variable
        subcategory_data = data.subcategory_data
        // get length of subcategories
        length_subcategory_data = subcategory_data.length

        // put options on dropdown
        for(var j = 0; j < length_subcategory_data; j++){
            option = put_options_here
            .append("option")
            .attr("value",subcategory_data[j].id)
            .text(subcategory_data[j].name)
            if(subcategory_data[j].name == value){
                option.attr("selected","selected")
            }

        }
    })
}
