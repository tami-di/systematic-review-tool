// what to do if the add-data-to-category button is pressed
d3.selectAll("#categorias").selectAll(".btn-success").on("click", function(){
    // get category id
     cat_name = d3.select(this).attr("value")
     // if authors do sth different
     if(cat_name == 'authors'){
         title_message = d3.select("#add-data-message")
         title_message.text("Add new author")
         form_body = d3.select("#add-data-body")
         // set action to form
         form = d3.select(form_body.node().parentNode)
         form.attr("action","/api/add/author/")
         // remove last elements of the form
         d3.select("#add-data-body").selectAll(".form-group").remove()
         form_group = form_body.append("div").attr("class","form-group")
         element_id_name = "author-name"
         element_id_affiliation = "author-affiliation"
         text_label_name = "name"
         text_label_affiliation = "affiliation"
         value = ""
         placeholder_name = "Insert author name"
         placeholder_affiliation = "Insert author affiliation"
         set_varchar_input (form_group,element_id_name,text_label_name,value,placeholder_name)
         form_group = form_body.append("div").attr("class","form-group")
         set_text_input(form_group,element_id_affiliation,text_label_affiliation,value,placeholder_affiliation)
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
         return
     }
     parent = this.parentNode
     cat_id = d3.select(parent).select(".btn-grey").attr("value")
     d3.json("/api/request/headers+subcategories/"+ cat_id,
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
             title_message.text("Add data to " + cat_name.trim())
             form_body = d3.select("#add-data-body")
             // set action to form
             form = d3.select(form_body.node().parentNode)
             form.attr("action","/api/add/data/category/" + cat_id)
             // remove last elements of the form
             d3.select("#add-data-body").selectAll(".form-group").remove()
             for(var i = 0; i < length; i++){
                 form_group = form_body.append("div").attr("class","form-group")
                 type = subcategories[i].type
                 subcat_id = subcategories[i].id
                 element_id = "sub-"+subcategories[i].name+"-cat-"+cat_id
                 text_label = subcategories[i].name
                 value = ""
                 if(type == 'varchar'){
                     placeholder = "Insert "+subcategories[i].name
                     set_varchar_input (form_group,element_id,text_label,value,placeholder)
                 }
                 if(type == 'text'){
                     placeholder = "Insert "+subcategories[i].name
                     set_text_input(form_group,element_id,text_label,value,placeholder)
                 }
                 if(type == 'number'){
                     placeholder = "-"
                     set_number_input(form_group,element_id,text_label,value,placeholder)
                 }
                 if(type == 'subcat'){
                     value = ""
                     name = (subcategories[i].interaction+subcategories[i].name).split(" ").join("_")
                     element_id = "sub-"+name+"-cat-"+cat_id
                     text_label = (subcategories[i].interaction).substring('has_'.length).split(" ").join(" ") +" "
                     + text_label
                     console.log(text_label)
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
 
     ///////
 
     // get subcategories of current category
     d3.json("/api/request/headers+subcategories/norep/"+ cat_id,
     function(error, data){
         if (error){
             console.log(error);
             return
         }
 
         // save subcategories into variable
         subcategories = data.subcategories
         // get length of subcategories
         length = subcategories.length
         set_title = true
         // set a button for each subcategory
         for(var i = 0; i < length; i++){
            if(subcategories[i].type == 'subcat'){ //no entra en este if (?)
                 if(set_title){
                     set_title = false
                     d3.select("#subcategorias")
                         .attr("class","panel-group col-md-3")
                         .append("div")
                         .attr("class","row")
                         .append("div")
                         .attr("class","col-md-12")
                         .append("h4")
                         .attr("class","text-center")
                         .text("Metacategories of category " + cat_name)
                 }
 
                 subcategory_buttons_container = d3.select("#subcategorias")
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
                 .attr("value",subcategories[i].interaction+"."+subcategories[i].name)
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
                 .attr("value",subcategories[i].interaction+"."+subcategories[i].name)
                 .append("i")
                 .attr("class","fa fa-plus-circle fa-lg")

                // set info subcategory button
                subcategory_buttons_container.append("button")
                .attr("type","button")
                .attr("id","info-subcat-" + cat_id + "." + subcategories[i].id)
                .attr("name","info-subcat-" + cat_id + "." + subcategories[i].id)
                .attr("data-toggle","modal")
                .attr("data-target","#info-data-modal")
                .attr("class","btn btn-primary")
                .attr("value",subcategories[i].interaction+"."+subcategories[i].name)
                .append("i")
                .attr("class","fa fa-info-circle fa-lg")
             }
         }
         // what to do if the add-data-to-subcategory button is pressed
         d3.selectAll("#subcategorias").selectAll(".btn-success").on("click", function(){
             // get category id
             value = d3.select(this).attr("value").split(".")
             subcat_interaction = value[0]
             subcat_name = value[1]
             parent = this.parentNode
             id = (d3.select(parent).select(".btn-grey").attr("value")).split(".")
             cat_id = id[0]
             subcat_id = id[1]
             d3.json("/api/request/headers+subcategories/norep/"+ cat_id,
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
                     title_message.text("Add data to " + subcat_name.trim())
                     form_body = d3.select("#add-data-body")
                     // set action to form
                     form = d3.select(form_body.node().parentNode)
                     form.attr("action","/api/add/data/category/" + cat_id + "/subcategory/" + subcat_id)
                     // remove last elements of the form
                     form.selectAll(".form-group").remove()
                     d3.select("#add-data-body").selectAll(".form-group").remove()
                     for(var i = 0; i < length; i++){
 
                         type = subcategories[i].type
                         if(type == 'subcat'){
                             if(subcategories[i].id == subcat_id){
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
                                         placeholder = "Insert "+name
                                         set_varchar_input(form_group,element_id,text_label,value,placeholder)
                                     }
                                     if(property_type == 'text'){
                                         placeholder = "Insert "+name
                                         set_text_input(form_group,element_id,text_label,value,placeholder)
                                     }
                                     if(property_type == 'number'){
                                         placeholder = "-"
                                         set_number_input(form_group,element_id,text_label,value,placeholder)
                                     }
 
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
             value = d3.select(this).attr("value").split(".")
             subcat_interaction = value[0]
             subcat_name = value[1]
             parent = this.parentNode
             id = (d3.select(parent).select(".btn-grey").attr("value")).split(".")
             cat_id = id[0]
             subcat_id = id[1]
             d3.select("#table-placer").selectAll("table").remove()
             d3.select("#table-placer").selectAll("h3").remove()
             d3.select("#table-placer").append("h3").text(subcat_name)
             the_table = d3.select("#table-placer")
             .append("table")
             .attr("class","table table-bordered table-striped table-hover table-responsive")
 
             d3.json('/api/request/data/subcategory/'+subcat_id,
                 function(error, data){
                     if (error){
                         console.log(error);
                         return
                     }
                 column_headers = data.column_headers
                 column_headers_length = column_headers.length
                 header_row = the_table.append("thead").append("tr")
                 for(var i = 0; i < column_headers_length; i++){
                     if(column_headers[i].name == 'id'){
                         continue
                     }
                     header_row.append("td")
                     .text(column_headers[i].name)
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
                         if(column_headers[k].name == 'id'){
                             continue
                         }
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
                         title_message.text("Modify data of " + cat_name.trim())
                         form_body = d3.select("#modify-data-body")
                         // set action to form
                         form = d3.select(form_body.node().parentNode)
                         form.attr("action",'/api/edit/category/'+cat_id+'/subcategory/'+subcat_id+'/row/'+
                         column_data[row]['id'])
                         // remove last elements of the form
                         d3.select("#modify-data-body").selectAll(".form-group").remove()
                         for(var i = 0; i < length; i++){
                             if(column_headers[i].name == 'id'){
                                 continue
                             }
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
                     .attr("data-target","#delete-element-modal")
                     .on("click",function(){
                         // set modal form parameter to delete row
                         row = d3.select(this).attr("value")
                         d3.select("#delete-element-message")
                            .text("Do you really want to delete \"" + d3.select(this).attr("value") + "\"?")
                         d3.select("#delete-form")
                         .attr("action",'/api/delete/data/subcategory/'+subcat_id+'/row/'+column_data[row]['id'])
                     })
                     .append("i")
                     .attr("class","fa fa-trash fa-lg")
 
 
                 }
             })
         })
     })
 
 
 
 })

 var lastClicked = null;
 // what to do if the see-all-data-of-category button is pressed
 d3.selectAll("#categorias").selectAll(".btn-info").on("click", function(){
         cat_name = d3.select(this).attr("value")
         parent = this.parentNode
         cat_id = d3.select(parent).select(".btn-grey").attr("value")

          // Check if the clicked category is the same as the last one
        if (lastClicked === cat_id) {
            // Toggle the visibility of the table
            var tablePlacer = d3.select("#table-placer");
            var table = tablePlacer.select("table");
            tablePlacer.selectAll("table, h3").remove();  // Remove existing table and header
            lastClicked = null;  // Reset lastClickedCategoryId
        } else {
            d3.select("#table-placer").selectAll("table").remove()
            d3.select("#table-placer").selectAll("h3").remove()
            d3.select("#table-placer").append("h3").text(cat_name)
            the_table = d3.select("#table-placer")
            .append("table")
            .attr("class","table table-bordered table-striped table-hover table-responsive")
            d3.json("/api/request/data/category/"+ cat_id ,
                function(error, data){
                    if (error){
                        console.log(error);
                        return
                    }
                column_headers = data.column_headers
                column_headers_length = column_headers.length
                header_row = the_table.append("thead").append("tr")
                for(var i = 0; i < column_headers_length; i++){
                    if(column_headers[i].name == 'id'){
                        continue
                    }
                    header_row.append("td")
                    .text(column_headers[i].name)
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
                        if(column_headers[k].name == 'id'){
                            continue
                        }
                        name_from_header_row = (column_headers[k].name).split(" ").join("")
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
                        console.log(row)
                        // save subcategories into variable
                        subcategories = column_headers
                        console.log(subcategories)
                        // get length of subcategories
                        length = subcategories.length
                        title_message = d3.select("#modify-data-message")
                        title_message.text("Modify data of " + cat_name.trim())
                        form_body = d3.select("#modify-data-body")
                        // set action to form
                        form = d3.select(form_body.node().parentNode)
                        form.attr("action",'/api/edit/category/'+cat_id+'/row/'+d3.select(this).attr("value"))
                        // remove last elements of the form
                        d3.select("#modify-data-body").selectAll(".form-group").remove()
                        for(var i = 0; i < length ; i++){
                            if(column_headers[i].name == 'id'){
                                continue
                            }
                            form_group = form_body.append("div").attr("class","form-group")
                            type = subcategories[i].type
                            subcat_id = subcategories[i].id
                            // set parameters for each type of input
                            name = (column_headers[i].name).split(" ").join("")
                            value = set_str_as_array(column_data[row][name])
                            placeholder = ""
                            element_id = "sub-"+(subcategories[i].name).split(" ").join("-")+"-cat-"+cat_id
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
                        .attr("data-target","#delete-element-modal")
                        .on("click",function(){
                            // set modal form parameter to delete row
                            row = d3.select(this).attr("value");
                            d3.select("#delete-form")
                                .attr("action",'/api/delete/data/category/'+cat_id+'/row/'+d3.select(this).attr("value"));
                        })
                        .append("i")
                        .attr("class","fa fa-trash fa-lg")
    
                }
    
            })
            lastClicked = cat_id;
        }
 
 });




 
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
     .attr("multiple","multiple")
     d3.json("/api/request/headers/subcategory/"+subcat_id,
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
             option = d3.select("#"+id)
             .append("option")
             .attr("value",subcategory_data[j].id)
             .text(subcategory_data[j].name)
             option
             .property("selected",function(d,i){
                 for (var i=0; i< value.length; i++){
                     if (d3.select(this).text() == value[i]){
                         return true
                     }
                 }
             })
             /*if(subcategory_data[j].name == value){
                 option.attr("selected","selected")
             }*/
 
         }
     })
 }
 
 var set_str_as_array = function(string){
     array_1 = string.split(";")
     array_2 = []
     for(i = 0; i < array_1.length; i++){
         if(array_1[i]!=''){
             array_2.push(array_1[i])
         }
     }
     return array_2
 }