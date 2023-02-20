<template>
  <div class="listadding" style="position:relative; min-height: 100vh; margin: 0px; background: linear-gradient(to bottom, #7D9CB6 0%, #785A6B 100%);">
    <div align="middle">
        <p class="alert alert-danger" v-if="error">{{ error }}</p>
    </div>
    <div align="right">
        <router-link :to="`/home`">
            <button style="height: 30px; width: 90px; border: 1px solid black; color: black">Home</button>
        </router-link> | 
        <button @click="exportLists" style="height: 30px; width: 90px; border: 1px solid black; color: black">Export</button> |
        <router-link :to="`/summary`">
            <button style="height: 30px; width: 90px; border: 1px solid black; color: black">Summary</button>
        </router-link> |
        <router-link :to="`/`">
            <button @click="clean" style="height: 30px; width: 90px; border: 1px solid black; color: black">Logout</button>
        </router-link>
    </div>
    <div align="middle" style="left:460px; top: 40px; position: absolute; margin: 60px; box-shadow:10px 10px 15px 15px #FAF136; background: wheat">
    <h3 align="center" style="color: black">Add List</h3>
    <div class="container" style="font-size: 1.5rem; display: inline-block; margin: 10px 50px 20px;">
    <div class="row" style="position: relative; margin: 50px 48px 50px;">
    <label style="color: black"><strong>List Name</strong></label>
    <input type="text" name="listname" v-model="listname" placeholder="Please enter list name" style="height: 20px" required/>
    </div>
    <div class="row" style="position: relative; margin: 50px 48px 50px;">
    <label style="color: black"><strong>List Description</strong></label>
    <input type="text" name="listdescription" v-model="listdescription" placeholder="list description....." style="height: 20px"/>
    </div>
    </div>
    <div class="row" style="margin: 10px 48px 20px;"></div>
    <button style="padding: 14px 40px; background-color: white; color: black; border: 2px solid black; border-radius: 50%; margin: 10px 48px 20px;" type="submit" @click="addList">Add List</button>
    </div>
    </div>
</template>

<script>
    export default {
        name: "ListAdding",
        data() {
            return {
                email: null,
                auth_token: null,
                lists: [],
                error: "",
                listname: null,
                listdescription: null
            };
        },
        mounted() {
            this.email=sessionStorage.getItem("email");
            this.auth_token=sessionStorage.getItem("auth-token");
            if(!this.auth_token){
                alert("Login to view your Dashboard")
                this.$router.push("/")
            }
        },
        methods: {
            async clean() {
                sessionStorage.clear()
                localStorage.clear()
            },
            async addList() {
                if(!this.listname) {
                    this.error = "List Name can not be empty";
                }
                else {
                    try {
                        fetch("http://127.0.0.1:5000/api/list/"+`${this.email}`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json;charset=utf-8",
                                "Authentication-Token": `${this.auth_token}`,
                            },
                            body: JSON.stringify({
                                email: this.email,      
                                list_name : this.listname,
                                list_description : this.listdescription
                            }),
                        })
                        .then((resp) =>  resp.json())
                        .then((data) => {
                            const response = data;
                            if (response.message) {
                                this.error = response.message;
                                console.log(response.message);
                            } else {
                                this.lists = data;
                                console.log(this.lists);
                                console.log("List Added");
                                this.$router.push("home");
                                console.log("its dashboard returns");
                            }
                        })
                        .catch((error) => {
                            console.log("1st",error);
                        });
                    } catch (error) {
                        console.log("2nd",error);
                    }
                }
            }
        }
    }

</script>

<style>

</style>