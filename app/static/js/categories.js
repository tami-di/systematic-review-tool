d3.selectAll("#categorias").selectAll(".btn-grey").on("click", function(){
            // get category id
            cat_id = d3.select(this).attr("id")
            // set clicked item active, set rest unactive
            set_active("#categorias",this)
            // remove last subcategories shown
            d3.select("#subcategorias").selectAll("div").remove()
            d3.select("#subcategorias").selectAll("button").remove()
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
                d3.select("#subcategorias")
                .attr("class","panel-group col-md-2")
                .append("div")
                .attr("class","row")
                .append("div")
                .attr("class","col-md-12")
                .append("h4")
                .attr("class","text-center")
                .text("Subcategorias de la Categoria " + cat_id)
                // set a button for each subcategory
                for(var i = 0; i < length; i++){
                    d3.select("#subcategorias").
                    append("div").
                    attr("class","panel panel-default").
                    attr("id","panel-default-"+i).
                    append("div").
                    attr("class","panel-heading").
                    append("h4").
                    attr("class","panel-title").
                    append("a").
                    attr("data-toggle","collapse").
                    attr("data-parent","#subcategories").
                    attr("href","#ccollapse"+i).
                    text(subcategories[i].name)

                    d3.select("#panel-default-"+i)
                    .append("div")
                    .attr("id","ccollapse"+i)
                    .attr("class","panel-collapse collapse")
                    .append("div")
                    .attr("class","panel-body")
                    .attr("id","collapse-body"+i)
                    // set properties and delete button on collapsable
                    properties = subcategories[i].properties
                    properties_length = properties.length
                    for(var j=0; j < properties_length; j++){
                        d3.select("#collapse-body"+i)
                        .append("div")
                        .attr("class","row container")
                        .text(properties[j])
                    }
                    d3.select("#collapse-body"+i)
                    .append("div")
                    .attr("class","row container")
                    .append("button")
                    .attr("class","btn btn-danger")
                    .text("Eliminar")
                    .attr("href","#")
                    .attr("data-toggle","modal")
                    .attr("value",i+"")
                    .attr("data-target","#delete-element-modal")
                    .on("click", function(){
                        // do stuff (show a warning message first)

                        var index = parseInt(d3.select(this).attr("value"))
                        d3.select("#delete-element-message")
                        .text("Estás seguro de que quieres eliminar " + subcategories[index].name + "?")

                        d3.select("#deleted-element")
                        .attr("value",cat_id + "." +subcategories[index].id)
                    })

                }
                // set_success_button(parent-of-button, button-id, button-text)
                set_success_button("#subcategorias", "add-subcat", "Añadir subcategoría")
                d3.select("#add-subcat").
                attr("href","#").
                attr("data-toggle","modal").
                attr("data-target","#add-subcategory-modal")
                // set value of hidden input
                d3.select("#category-of-subcategory")
                .attr("value",""+cat_id)
            })
        })

d3.selectAll("#categorias").selectAll(".btn-danger").on("click", function(){
        d3.select("#delete-element-message")
        .text("Estás seguro de que quieres eliminar " + d3.select(this).attr("value") + "?")

        var cat_id = d3.select(this.parentNode.parentNode).selectAll(".btn-grey").attr("id")

        d3.select("#deleted-element")
        .attr("value",cat_id)
})

var set_active = function(id, object){
                    d3.selectAll(id).selectAll("button").
                    classed("active", false)
                    d3.select(object).
                    classed("active", true)
                }

var set_success_button = function(parent_id, button_id, message){
                            d3.select(parent_id).
                            append("button").
                            attr("class", "btn btn-success btn-ctnr").
                            attr("id", button_id).
                            text(message)
                        }