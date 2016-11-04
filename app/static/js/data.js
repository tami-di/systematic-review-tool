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