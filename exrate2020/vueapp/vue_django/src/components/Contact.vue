<template>

    <div class="contact-form-overlay col-md-8 offset-md-2 p-5">

        <div class="fancy-title title-border">
            <h3>Send us an Email</h3>
        </div>
        <div class="form-widget">

            <div class="form-result"></div>
            <h2>{{message}}</h2>

            <!-- Contact Form
            ============================================= -->
            <form class="row mb-0" action="{% url 'contact' %}" method="post">
                {% csrf_token %}

                {# {% if messages %}#}
                {#
                <ul class="messages">#}
                    {# {% for message in messages %}#}
                    {#
                    <li
                    {% if message.tags %}#}
                    {# class="{{ message.tags }}"{% endif %}>{{ message }}</li>#}
                    {# {% endfor %}#}
                    {#
                </ul>
                #}
                {# {% endif %}#}
                <div class="col-md-6 form-group">
                    <label for="name">Name <small>*</small></label>
                    <input type="text" id="name" name="name" value="" class="sm-form-control required"/>
                </div>

                <div class="col-md-6 form-group">
                    <label for="email">Email <small>*</small></label>
                    <input type="email" id="email" name="email" value=""
                           class="required email sm-form-control"/>
                </div>

                <div class="w-100"></div>

                <div class="col-12 form-group">
                    <label for="subject">Subject <small>*</small></label>
                    <input type="text" id="subject" name="subject" value=""
                           class="required sm-form-control"/>
                </div>

                <div class="col-12 form-group">
                    <label for="message">Message <small>*</small></label>
                    <textarea class="required sm-form-control" id="message" name="message" rows="6"
                              cols="30"></textarea>
                </div>

                <div class="col-12 form-group">
                    <input class="button button-3d m-0" type="submit" value="Send us Message"/>
                </div>

            </form>
        </div>

        <div class="line"></div>

        <div class="row col-mb-50">
            <!-- Contact Info
            ============================================= -->
            <div class="col-md-12">
                <address>
                    <strong>Headquarters:</strong><br>
                    795 Folsom Ave, Suite 600<br>
                    San Francisco, CA 94107<br>
                </address>
                <abbr title="Phone Number"><strong>Phone:</strong></abbr> (1) 8547 632521<br>
                <abbr title="Fax"><strong>Fax:</strong></abbr> (1) 11 4752 1433<br>
                <abbr title="Email Address"><strong>Email:</strong></abbr> info@canvas.com
            </div><!-- Contact Info End -->

            <!-- Testimonails
            ============================================= -->
            {#
            <div class="col-md-8">#}
                {#
                <div class="fslider customjs testimonial twitter-scroll twitter-feed" data-username="envato"
                     data-count="4" data-animation="slide" data-arrows="false">#}
                    {# <i class="i-plain color icon-twitter mb-0" style="margin-right: 15px;"></i>#}
                    {#
                    <div class="flexslider" style="width: auto;">#}
                        {#
                        <div class="slider-wrap">#}
                            {#
                            <div class="slide"></div>
                            #}
                            {#
                        </div>
                        #}
                        {#
                    </div>
                    #}
                    {#
                </div>
                #}
                {#
            </div>
            #}
        </div>

    </div><!-- Contact Form Overlay End -->
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
