<template>
    <div class="delCard" align="middle">
        <h2 style="position:relative; margin: 300px 70px 50px">
            Are you sure you want to delete the card ?
        </h2>
        <button @click="deleteCard" style="height: 70px; width: 150px; font-size: 1.5rem; border: 2px solid #8B0000; color: red">YES</button> &nbsp; &nbsp;
        <a href="/home"><button style="height: 70px; width: 150px; font-size: 1.5rem; border: 2px solid #0B6C1B; color: green">NO</button></a>
    </div>
</template>
<script>
    export default {
        name: 'CardDelete',
        data() {
            return {
                cardid:null,
                error: "",
                auth_token: null,
                email: null
            };
        },
        async created() {
            this.cardid = localStorage.getItem("cid");
            this.auth_token = sessionStorage.getItem("auth-token")
            if(!this.auth_token){
                alert("Login to view your Dashboard")
                this.$router.push("/")
            }
            this.email = sessionStorage.getItem("email")
            console.log(this.cardid);
        },
        methods:{
            deleteCard() {
                try{
                    fetch(`http://127.0.0.1:5000/api/card/${this.email}/${this.cardid}`,{
                        method: "DELETE",
                        headers:{
                            "Content-Type" : "application/json",
                            "Authentication-Token":`${this.auth_token}`
                        }
                    })
                    .then((resp) =>  resp.json())
                    .then((data) => {
                        const response = data;
                        console.log(response)
                        if (response.message) {
                            this.error = response.message;
                            console.log(response.message);
                        } else {
                            console.log("Card Deleted");}
                            this.$router.go(-1);
                        }).catch((error) => {
                            console.log("1st",error);
                        });
                    }catch(error){
                        console.log("2nd",error)
                    }
                }
            },
        };
</script>