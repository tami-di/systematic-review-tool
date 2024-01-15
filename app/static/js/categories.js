var catShown = false;
var lastClickedCategoryId = null; // Added variable to store the last clicked category ID

// show subcategories and properties of category
d3.selectAll("#categorias").selectAll(".btn-grey").on("click", function() {
    // get category id
    var cat_id = d3.select(this).attr("id");
    var cat_name = d3.select(this).text();

    // Check if the same button is pressed twice
    if (catShown && lastClickedCategoryId === cat_id) {
        // hide subcategories if the category is clicked again
        d3.select("#subcategorias").selectAll("table").remove();
        d3.select("#subcategorias").selectAll("button").remove();
        d3.select("#subcategorias").selectAll("div").remove();
        catShown = false;
    } else {
        // set clicked item active, set rest unactive
        set_active("#categorias", this);

        // Remove last subcategories shown only if a different category is clicked
        if (lastClickedCategoryId !== cat_id) {
            d3.select("#subcategorias").selectAll("table").remove();
            d3.select("#subcategorias").selectAll("button").remove();
            d3.select("#subcategorias").selectAll("div").remove();
        }

        // get subcategories of current category
        d3.json("/api/request/headers+subcategories/" + cat_id, 
            function(error, data) {
                if (error){
                    console.log(error);
                    return;
                }
                // save subcategories into variable
                subcategories = data.subcategories;
                // get length of subcategories
                length = subcategories.length;
    
                // table structure
                table = d3.select("#subcategorias")
                    .append("table")
                    .attr("class", "table table-bordered table-striped table-responsive")
                    .style("margin", "25px 0")
                    .style("min-width", "400px");
    
                // set table header
                table.append("thead")
                    .append("tr")
                    .append("th")
                    .attr("colspan", "4")
                    .append("h4")
                    .text("Metacategories and other criteria of " + "\r\n" + cat_name[0].toUpperCase() + cat_name.substring(1))
                    .style("padding", "10px")
                    .style("text-align", "center")
                    .attr("class", "text-center");
                
                
    
                // set table body
                tbody = table.append("tbody");
                

            
                for (var i = 0; i < length; i++) {
                    row = tbody.append("tr");
                    type = subcategories[i].type;
    
                    if (type == 'subcat') { //no entra 
                        row.append("td")
                            .text("Metacategory")
                        cell = row.append("td")
                            .text((subcategories[i].interaction).split('_').join(' ') + " " + subcategories[i].name);
                    } else {
                        row.append("td")
                            .text("Name")
                            .style("font-weight", "bold");
                        cell = row.append("td")
                            .text(subcategories[i].name);

                        row.append("td")
                            .text("Type")
                            .style("font-weight", "bold");
                        row.append("td")
                            .text(subcategories[i].type);
                    }
                    
    
                    var isRowAdded = false;
                    // add delete button on subcategory or column of category
                    if ((subcategories[i].name != "description") && (subcategories[i].name != "name")) {
    
                        cell.style("cursor", "pointer")
                            .on("mouseover", function() {
                                d3.select(this).style("background-color", "#efefef");
                            })
                            .on("mouseout", function() {
                                d3.select(this).style("background-color", "initial");
                            });
                        
    
    
                        cell.on("click", function () {
                            if(!isRowAdded){
                                var newRow = tbody.append("tr").attr("class", "delete-row");
                                newRow.append("button")
                                    .attr("class", "btn btn-danger btn-ctnr")
                                    .text("Delete")
                                    .style("width","100%")
                                    .attr("href", "#")
                                    .attr("data-toggle", "modal")
                                    .attr("value", i-1 + "")
                                    .attr("data-target", "#delete-element-modal")
                                    .on("click", function () {
                                        var index = parseInt(d3.select(this).attr("value"));
                                        d3.select("#delete-element-message")
                                            .text("Do you really want to delete \"" + subcategories[index].name + "\"?");
                                        if(subcategories[index].is_subcat){
                                            // in case of deleting a subcategory
                                            subcat_id = subcategories[index].id;
                                            d3.select("#delete-form")
                                                .attr("action","/api/delete/subcategory/"+subcat_id+"/category/"+cat_id);
                                        }else{
                                            // in case of deleting a column of a category
                                            column_name = subcategories[index].name;
                                            d3.select("#delete-form")
                                                .attr("action",'/api/delete/column/'+column_name+'/category/'+cat_id);
                                        }
                                        d3.select("#deleted-element")
                                            .attr("value",cat_id + "." +subcategories[index].name);
                                
                                    });
                                isRowAdded = true;
                                }
                            else {
                                d3.select("tr.delete-row").remove();
                                isRowAdded = false;
                            }     
    
                        });
                    }
    
                    // set success buttons container
                    var successButtonContainer = d3.select("#subcategorias")
                        .append("div")
                        .attr("class", "content-container")
                        .attr("id", "subcat-btn-container");
    
                    if (subcategories[i].is_subcat) {
                        // append add column button on subcategory
                        cell.append("button")
                            .attr("class", "btn btn-success btn-ctnr-collapsable")
                            .text("Add criteria")
                            .attr("href", "#")
                            .attr("data-toggle", "modal")
                            .attr("value", i + "")
                            .attr("data-target", "#add-column-modal")
                            .on("click", function () {
                                // set personalized message on modal
                                d3.select("#add-column-message")
                                    .text("Insert new criteria in category \"" + cat_name + "\"");
                                // put proper action in form
                                action_url = '/api/add/column/category/'+cat_id;
                                d3.select("#add-column-form")
                                    .attr("action",action_url);
                            });
                    }
                }
    
                // set add metacategory button
                var successButtonContainer = d3.select("#subcategorias")
                    .append("div")
                    .attr("class", "content-container")
                    .attr("id", "subcat-btn-container");
    
                successButtonContainer.append("div")
                    .attr("class","content-container")
                    .attr("id","subcat-btn-container")
                    // set_success_button(parent-of-button, button-id, button-text)
                    set_success_button("#subcat-btn-container", "add-subcat", "Add metacategory")
                
                d3.select("#add-subcat")
                    .attr("href","#")
                    .attr("data-toggle","modal")
                    .attr("data-target","#add-subcategory-modal")
                    .on("click",function(){
                        d3.json("/api/request/data/subcategories/category/"+cat_id,
                            function(error, data){
                                if (error){
                                    console.log(error);
                                    return
                                }
                                subcategories = data.subcategories_info
                                select = d3.select("#select-existig-subcat")
                                select.selectAll("option").remove()
                                select.append("option")
                                    .attr("value",0)
                                    .text("Create new metacategory")
    
                                for(i = 0; i < subcategories.length ; i++){
                                    select.append("option")
                                        .attr("value",subcategories[i].subcat_id)
                                        .text(subcategories[i].subcat_name)
                                }
                            })
                    })
    
                // set value of hidden input
                d3.select("#category-of-subcategory")
                    .attr("value",""+cat_id)
    
                // set add criteria button
                set_success_button("#subcat-btn-container", "add-cat-col", "Add criteria")
                // here columns of data are added to a category
                d3.select("#add-cat-col")
                    .attr("href","#")
                    .attr("data-toggle","modal")
                    .attr("data-target","#add-column-modal")
                    .on("click",function(){
                        // set personalized message on modal
                        d3.select("#add-column-message")
                            .text("Insert new criteria in category \"" + cat_name + "\"")
                        // put proper action in form
                        action_url = '/api/add/column/category/'+cat_id
                        d3.select("#add-column-form")
                            .attr("action",action_url)
                    })
    
                // delete categories action
                d3.selectAll("#categorias").selectAll(".btn-danger").on("click", function(){
                    // first ask if sure (may be miss-click)
                    d3.select("#delete-element-message")
                        .text("Do you really want to delete \"" + d3.select(this).attr("value") + "\"?")
                    // get category id
                    var cat_id = d3.select(this.parentNode.parentNode).selectAll(".btn-grey").attr("id")
                    // if the delete button is pressed on the form then the category is permanently deleted
                    d3.select("#delete-form").attr("action","/api/delete/category/"+cat_id)
                });
                    
        });
    

        // Update the last clicked category ID
        lastClickedCategoryId = cat_id;
        catShown = true;
        
    }
});

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
