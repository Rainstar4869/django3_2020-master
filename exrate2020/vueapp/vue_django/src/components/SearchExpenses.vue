<template>
    <div>
        <div class="row">

            <div class="col-md-2">


                <a href="/expenses/add" class="btn btn-primary">Add Expense</a>
            </div>
            <div class="col-md-10">

                <div class="dropdown float-right">
                    <a class="btn btn-secondary dropdown-toggle" href="#" role="button" id="dropdownMenuLink"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        PerPage
                    </a>

                    <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                        <a class="dropdown-item" href="/expenses/top?page=1&per_page=10">10</a>
                        <a class="dropdown-item" href="/expenses/top?page=1&per_page=50">50</a>
                        <a class="dropdown-item" href="/expenses/top?page=1&per_page=100">100</a>
                    </div>
                </div>
                <div class="form-group float-right">
                    <input type="text" class="form-control" id="vue_searchField" v-model="keyval" v-on:keyup="search_db"
                           placeholder="Search">
                </div>
            </div>
        </div>
        <div >
            <table class="table table-stripped table-hover">
                <thead v-show="showTableHeader">
                <tr>
                    <th>Amount</th>
                    <th>Category</th>
                    <th>Description</th>
                    <th>Date</th>
                    <th></th>
                </tr>
                </thead>

                <tbody class="search-table">
                <tr v-for="expense in expenses">
                    <td>{{ expense.amount }}</td>
                    <td>{{ expense.category }}</td>
                    <td>{{ expense.description }}</td>
                    <td>{{ expense.date }}</td>

                    <td>
                        <!--                        {# <a href="{% url 'expense-edit' expense.id %}" class="btn btn-secondary btn-sm">Edit</a>#}-->
                    </td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>

</template>

<script>
import {getCookie} from "../utils/common.js"

export default {
    name: 'searchexpenses',
    props:["user"],
    data() {
        return {
            expenses:[],
            keyval:""
        }
    },
    created() {
    },
    computed:{
      showTableHeader(){
          return this.keyval.length!==0;
      }
    },
    methods:{
        ready_for_search(){
          console.log("ready for search");
        },
        search_db() {
            const appTable = document.querySelector(".app_table_section");
            console.log(appTable);
            const searchTable = document.querySelector(".search-table");

            if (this.keyval.length > 0) {
                appTable.style.display="none";
                // searchTable.style.display="block";
                axios.post("/expenses/search-expenses", {
                    searchText: this.keyval
                }).then(res => {
                    console.log(res.data);
                    this.expenses = res.data;
                })
            }else{

                appTable.style.display="block";
                searchTable.style.display="none";

            }

        }
    }
}
</script>

<style>

</style>
