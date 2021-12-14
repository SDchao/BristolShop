<template>
    <div class="title">
        <h1>究极无敌超市比价</h1>
        <div class="input-field">
            <el-input v-model="kw" clearable placeholder="请输入商品名称"
                      style="margin: 5px;"></el-input>
            <el-button type="primary"
                       style="margin: 5px;"
                       @click="queryItem"
                       :disabled="!canQuery">搜索
            </el-button>
        </div>
    </div>
    <div class="result" style="margin-top: 10px">
        <el-table :data="tableData" stripe align="center" v-loading="!canQuery" size="mini">
            <el-table-column prop="name" label="名称" align="center">
                <template #default="scope">
                    <a :href="scope.row.url">{{ scope.row.name }}</a>
                </template>
            </el-table-column>
            <el-table-column prop="imgurl" label="图片" align="center">
                <template #default="scope">
                    <el-image :src="scope.row.imgurl" lazy
                              style="max-width: 50px; max-height: 50px"/>
                </template>
            </el-table-column>
            <el-table-column prop="price" label="价格" sortable align="center"/>
            <el-table-column prop="store" label="来源" align="center"/>
            <el-table-column prop="unitprice" label="单价" align="center"/>
        </el-table>
    </div>

    <el-backtop/>
</template>

<script>
import {ElMessage} from 'element-plus'

export default {
    name: 'App',
    data() {
        return {
            kw: "",
            canQuery: true,
            tableData: []
        }
    },
    methods: {
        parseData(text) {
            try {
                let data = JSON.parse(text)
                this.tableData = data.items
            } catch (e) {
                ElMessage.error("无法获取商品列表")
            }

        },

        queryItem() {
            this.canQuery = false
            let request = new XMLHttpRequest()
            request.onreadystatechange = () => {
                this.canQuery = true
                if (request.readyState === 4) {
                    if (request.status === 200) {
                        this.parseData(request.responseText)
                    } else {
                        // Error
                        ElMessage.error("网络错误")
                    }
                }
            }

            request.open("GET", "/query/" + this.kw)
            request.send()
        }
    },
    setup() {
        document.title = "究极无敌超市比价"
    }
}
</script>

<style>
#app {
    display: flex;
    align-content: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
}

.title {
    margin: 5px 30px;
}

.input-field {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: space-between;
}
</style>
