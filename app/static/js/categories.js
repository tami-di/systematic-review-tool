// show subcategories and properties of category
d3.selectAll("#categorias").selectAll(".btn-grey").on("click", function(){
            // get category id
            cat_id = d3.select(this).attr("id")
            cat_name = d3.select(this).text()
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
                .text("\"" + cat_name + "\" subcategories and columns")
                // set a button for each subcategory
                for(var i = 0; i < length; i++){
                    collapse_title = d3.select("#subcategorias")
                    .append("div")
                    .attr("class","panel panel-default")
                    .attr("id","panel-default-"+i)
                    .append("div")
                    .attr("class","panel-heading")
                    .append("h4")
                    .attr("class","panel-title")
                    .append("a")
                    .attr("data-toggle","collapse")
                    .attr("data-parent","#subcategories")
                    .attr("href","#ccollapse"+i)
                    if(subcategories[i].type == 'subcat'){
                        collapse_title.text("Subcategory "+subcategories[i].name)
                    }else{
                        collapse_title.text(subcategories[i].name+" : "+subcategories[i].type)
                    }


                    d3.select("#panel-default-"+i)
                    .append("div")
                    .attr("id","ccollapse"+i)
                    .attr("class","panel-collapse collapse")
                    .append("div")
                    .attr("class","panel-body")
                    .attr("id","collapse-body"+i)
                    // set properties and delete button on collapsable
                    properties = subcategories[i].properties
                    properties_type = subcategories[i].properties_type
                    properties_length = properties.length
                    for(var j=0; j < properties_length; j++){
                        d3.select("#collapse-body"+i)
                        .append("div")
                        .attr("class","row container")
                        .text(properties[j]+" : "+properties_type[properties[j]])
                    }
                    // append delete button on subcategory or column of category
                    d3.select("#collapse-body"+i)
                    .append("div")
                    .attr("class","row container")
                    .append("button")
                    .attr("class","btn btn-danger btn-ctnr-collapsable")
                    .text("  Delete  ")
                    .attr("href","#")
                    .attr("data-toggle","modal")
                    .attr("value",i+"")
                    .attr("data-target","#delete-element-modal")
                    .on("click", function(){
                        // do stuff (show a warning message first)
                        var index = parseInt(d3.select(this).attr("value"))
                        d3.select("#delete-element-message")
                        .text("Do you really want to delete \"" + subcategories[index].name + "\"?")
                        if(subcategories[index].is_subcat){
                            // in case of deleting a subcategory
                            subcat_id = subcategories[index].id
                            d3.select("#delete-form")
                            .attr("action","/api/delete_subcategory/"+subcat_id+"/category/"+cat_id)
                        }else{
                            // in case of deleting a column of a category
                            column_name = subcategories[index].name
                            d3.select("#delete-form")
                            .attr("action",'/api/delete_column/'+column_name+'/category/'+cat_id)
                        }
                        d3.select("#deleted-element")
                        .attr("value",cat_id + "." +subcategories[index].name)
                    })
                    // append add column button on subcategory or column of category
                    if(subcategories[i].is_subcat){
                        d3.select("#collapse-body"+i)
                        .append("div")
                        .attr("class","row container")
                        .append("button")
                        .attr("class","btn btn-success btn-ctnr-collapsable")
                        .text("Add column")
                        .attr("href","#")
                        .attr("data-toggle","modal")
                        .attr("value",i+"")
                        .attr("data-target","#add-column-modal")
                        .on("click", function(){
                            var index = parseInt(d3.select(this).attr("value"))
                            // set personalized message on modal
                            d3.select("#add-column-message")
                            .text("Insert new column in subcategory \"" + subcategories[index].name + "\"")
                            subcat_id = subcategories[index].id
                            // put proper action in form
                            action_url = '/api/add_column/'+subcat_id+'/subcategory'
                            d3.select("#add-column-form")
                            .attr("action",action_url)
                        })
                    }


                }
                d3.select("#subcategorias")
                .append("div")
                .attr("class","content-container")
                .attr("id","subcat-btn-container")
                // set_success_button(parent-of-button, button-id, button-text)
                set_success_button("#subcat-btn-container", "add-subcat", "Add subcategory")
                d3.select("#add-subcat").
                attr("href","#").
                attr("data-toggle","modal").
                attr("data-target","#add-subcategory-modal")
                // set value of hidden input
                d3.select("#category-of-subcategory")
                .attr("value",""+cat_id)

                // set_success_button(parent-of-button, button-id, button-text)
                set_success_button("#subcat-btn-container", "add-cat-col", "Add column")
                // here columns of data are added to a category
                d3.select("#add-cat-col")
                .attr("href","#")
                .attr("data-toggle","modal")
                .attr("data-target","#add-column-modal")
                .on("click",function(){
                    // set personalized message on modal
                    d3.select("#add-column-message")
                    .text("Insert new column in category \"" + cat_name + "\"")
                    // put proper action in form
                    action_url = '/api/add_column/'+cat_id+'/category'
                    d3.select("#add-column-form")
                    .attr("action",action_url)
                })
            })
        })
// delete categories action
d3.selectAll("#categorias").selectAll(".btn-danger").on("click", function(){
        // first ask if sure (may be miss-click)
        d3.select("#delete-element-message")
        .text("Do you really want to delete \"" + d3.select(this).attr("value") + "\"?")
        // get category id
        var cat_id = d3.select(this.parentNode.parentNode).selectAll(".btn-grey").attr("id")
        // if the delete button is pressed on the form then the category is permanently deleted
        d3.select("#delete-form").attr("action","/api/delete_category/"+cat_id)
})
// set clicked element as 'active'
var set_active = function(id, object){
                    d3.selectAll(id).selectAll("button").
                    classed("active", false)
                    d3.select(object).
                    classed("active", true)
                }
// set a success (green) button on parent containig a message
var set_success_button = function(parent_id, button_id, message){
                            d3.select(parent_id).
                            append("button").
                            attr("class", "btn btn-success btn-ctnr-cat").
                            attr("id", button_id).
                            text(message)
                        }