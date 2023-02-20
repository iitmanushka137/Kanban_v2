<template>
    <div class="listupdating" style="position:relative; min-height: 100vh; margin: 0px; background: linear-gradient(to bottom, #DEDE33 0%, #4A65B2 100%);">
        <div align="middle">
            <p class="alert alert-danger" v-if="error">{{ error }}</p>
        </div>
        <div align="right" style="color: white">
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
        <h2 align="center" style="color: black">Update List</h2>
        <div align="middle" style="left:400px; top: 40px; position: absolute; margin: 60px; box-shadow:10px 10px 15px 15px #FAF136; background: wheat">
        <div class="container" style="font-size: 1.5rem; display: inline-block; margin: 10px 50px 20px;">
            <div class="row" style="position: relative; margin: 50px 48px 50px;">
                <label style="color: black"><strong>List Name</strong></label>
                <input type="text" name="listname" v-model="listname" placeholder="Please enter list name" style="height: 20px"/>
            </div>
            <div class="row" style="position: relative; margin: 50px 48px 50px;">
                <label style="color: black"><strong>List Description</strong></label>
                <input type="text" name="listdescription" v-model="listdescription" placeholder="list description....." style="height: 20px"/>
            </div>
        </div>
        <div class="row" style="margin: 10px 48px 20px;"></div>
        <button style="padding: 14px 40px; background-color: white; color: black; border: 2px solid black; border-radius: 50%; margin: 10px 48px 20px;" type="submit" @click="updateList(); clearLocal()">Update List</button>
        </div>
    </div>
</template>

<script>
    export default {
    name: "UpdateList",
    data() {
        return {
            listid:null,
            email: null,
            auth_token: null,
            error: "",
            listname: null,
            listdescription: null
        };
    },
    async created() {
        this.listid = localStorage.getItem("list_id");
        console.log(this.listid);
        this.email = sessionStorage.getItem("email");
        this.auth_token = sessionStorage.getItem("auth-token");
        if(!this.auth_token){
            alert("Login to view your Dashboard")
            this.$router.push("/")
        }
        this.listname = localStorage.getItem("listname")
        this.listdescription = localStorage.getItem("listdescription")
    },
    mounted() {
        this.email = sessionStorage.getItem("email");
        this.auth_token = sessionStorage.getItem("auth-token");
    },
    methods: {
        async clean() {
            sessionStorage.clear()
            localStorage.clear()
        },
        async updateList() {
            if (!this.listname) {
                this.listname = localStorage.getItem("listname");
            } else {
                console.log("all ok")
            try {
                fetch(`http://127.0.0.1:5000/api/list/${this.email}/${this.listid}`, {
                    method: "PUT",
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
                        console.log("List Updated");
                        this.$router.go(-1)
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
    },
        clearLocal(){
            localStorage.clear()
        }
  },
};
</script>