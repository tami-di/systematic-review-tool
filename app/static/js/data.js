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
                id = subcategories[i].id
                if(type == 'varchar'){
                    form_group.append("label")
                    .attr("class","col-md-4 control-label")
                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .text(subcategories[i].name)
                    form_group.append("div")
                    .attr("class","col-md-8")
                    .append("input")
                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("type","text")
                    .attr("placeholder","Inserte "+subcategories[i].name)
                    .attr("class","form-control input-md")
                }
                if(type == 'text'){
                    form_group.append("label")
                    .attr("class","col-md-4 control-label")
                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .text(subcategories[i].name)
                    form_group.append("div")
                    .attr("class","col-md-8")
                    .append("textarea")
                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("placeholder","Inserte "+subcategories[i].name)
                    .attr("class","form-control input-md")
                }
                if(type == 'number'){
                    form_group.append("label")
                    .attr("class","col-md-4 control-label")
                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .text(subcategories[i].name)
                    form_group.append("div")
                    .attr("class","col-xs-3")
                    .append("input")
                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("type","number")
                    .attr("placeholder","-")
                    .attr("class","form-control input-md")

                }
                if(type == 'subcat'){
                    // add label to dropdown
                    form_group.append("label")
                    .attr("class","col-md-4 control-label")
                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .text(subcategories[i].name)
                    // add dropdown
                    form_group.append("div")
                    .attr("class","col-md-8")
                    .append("select")
                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id)
                    .attr("class","form-control")
                    put_options_here = d3.select("#sub-"+subcategories[i].id+"-cat-"+cat_id)
                    d3.json("/api/category/"+ cat_id + "/subcategory_data/"+id,
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
                            put_options_here
                            .append("option")
                            .attr("value",subcategory_data[j].id)
                            .text(subcategory_data[j].name)
                        }
                    })
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
            div_for_buttons.append("button")
            .attr("id","accept-new-data")
            .attr("type","submit")
            .attr("name","accept-new-data")
            .attr("class", "btn btn-success")
            .text("Aceptar")

            div_for_buttons.append("button")
            .attr("id","cancel-new-data")
            .attr("data-dismiss","modal")
            .attr("name","cancel-new-data")
            .attr("class", "btn btn-danger")
            .text("cancelar")



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
                                if(property_type == 'varchar'){
                                    form_group.append("label")
                                    .attr("class","col-md-4 control-label")
                                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .text(name)
                                    form_group.append("div")
                                    .attr("class","col-md-8")
                                    .append("input")
                                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .attr("type","text")
                                    .attr("placeholder","Inserte "+name)
                                    .attr("class","form-control input-md")
                                }
                                if(property_type == 'text'){
                                    form_group.append("label")
                                    .attr("class","col-md-4 control-label")
                                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .text(name)
                                    form_group.append("div")
                                    .attr("class","col-md-8")
                                    .append("textarea")
                                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .attr("placeholder","Inserte "+name)
                                    .attr("class","form-control input-md")
                                }
                                if(property_type == 'number'){
                                    form_group.append("label")
                                    .attr("class","col-md-4 control-label")
                                    .attr("for","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .text(name)
                                    form_group.append("div")
                                    .attr("class","col-xs-3")
                                    .append("input")
                                    .attr("id","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .attr("name","sub-"+subcategories[i].id+"-cat-"+cat_id+"-"+name)
                                    .attr("type","number")
                                    .attr("placeholder","-")
                                    .attr("class","form-control input-md")
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
                    div_for_buttons.append("button")
                    .attr("id","accept-new-data")
                    .attr("type","submit")
                    .attr("name","accept-new-data")
                    .attr("class", "btn btn-success")
                    .text("Aceptar")

                    div_for_buttons.append("button")
                    .attr("id","cancel-new-data")
                    .attr("data-dismiss","modal")
                    .attr("name","cancel-new-data")
                    .attr("class", "btn btn-danger")
                    .text("cancelar")



                    })
        })

    })



})


var set_active = function(id, object){
                    d3.selectAll(id).selectAll("button").
                    classed("active", false)
                    d3.select(object).
                    classed("active", true)
                }