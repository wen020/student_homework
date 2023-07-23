<template>
    <div class="student-homework-wrap">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-fa fa-book"></i> 作业列表
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div class="container">
            <div class="query-form">
                <el-row :gutter="20">
                    <el-col :offset="15" :span="3">
                        <el-input @keyup.enter.native="query" onkeyup="value=value.replace(/[^\d]/g,'')"
                                  placeholder="作业编号" v-model="queryForm.homeworkId"/>
                    </el-col>
                    <el-col :span="3">
                        <el-input @keyup.enter.native="query" placeholder="作业标题" v-model="queryForm.homeworkTitle"/>
                    </el-col>
                    <el-col :span="3">
                        <el-button @click="query" icon="el-icon-search" type="primary">搜索</el-button>
                    </el-col>
                </el-row>
            </div>

            <div>
                <p></p>
            </div>

            <el-row justify="center" type="flex">
                <el-pagination
                        :current-page.sync="pageIndex"
                        :page-size="pageSize"
                        :total="pageSize * pageCount"
                        @current-change="getPage"
                        background
                        layout="prev, pager, next"
                >
                </el-pagination>
            </el-row>

            <div>
                <p></p>
            </div>

            <div class="table">
                <el-table :data="tableData" stripe>
                    <el-table-column label="作业编号" prop="homeworkId"/>
                    <el-table-column label="教师" prop="teacherName"/>
                    <el-table-column label="作业标题" prop="homeworkTitle"/>
                    <el-table-column label="作业内容" prop="homeworkContent" width="200px"/>
                    <el-table-column align="center" label="操作" width="200px">
                        <template slot-scope="scope">
                            <el-button @click="editStudentHomework(scope.row.homeworkId)" size="mini" type="success">
                                提交作业
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <el-dialog :visible.sync="editing" title="编辑" width="50%">
                <el-form :model="entityForm" label-width="82px" ref="form">
                    <el-form-item label="作业编号">
                        <el-input disabled type="number" v-model="entityForm.homeworkId"></el-input>
                    </el-form-item>
                    <el-form-item label="作业标题">
                        <el-input disabled type="text" v-model="entityForm.homeworkTitle"></el-input>
                    </el-form-item>
                    <el-form-item label="作业内容">
                        <el-input disabled type="textarea" v-model="entityForm.homeworkContent"></el-input>
                    </el-form-item>
                    <el-form-item label="提交的标题">
                        <el-input type="text" v-model="entityForm.title"></el-input>
                    </el-form-item>
                    <el-form-item label="提交的内容">
                        <el-input type="textarea" v-model="entityForm.content"></el-input>
                    </el-form-item>
                    <el-form-item label="上传文件:" prop="pdf">
                      <el-upload
                        class="upload-demo"
                        ref="upload"
                        action<!-- 这里比填,异步时写后端接口,就可以,我们不用,所以不谢-->
                        :http-request="httpRequest"<!--覆盖默认的上传行为，可以自定义上传的实现-->
                        :before-upload="beforeUpload"<!--这是上传前的处理方法-->
                        :on-exceed="handleExceed"<!--文件超出个数限制时的钩子-->
                        :limit="1">
                        <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
                        <div slot="tip" class="el-upload__tip">只能上传.pdf文件，且不超过5M</div>
                      </el-upload>
                    </el-form-item>
                </el-form>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="save" type="primary">确 定</el-button>
                    <el-button @click="editing = false">取 消</el-button>
                </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    import * as homeworkApi from "@/api/student/homework";

    export default {
        name: "StudentHomework",
        data() {
            return {
                queryForm: {
                    homeworkId: "",
                    homeworkTitle: ""
                },
                entityForm: {},
                tableData: [],
                pageSize: homeworkApi.pageSize,
                pageCount: 1,
                pageIndex: 1,
                editing: false
            };
        },
        methods: {
            httpRequest(option) {
                this.entityForm.fileList.push(option)
            },
            // 上传前处理
            beforeUpload(file) {
                let fileSize = file.size
                const FIVE_M= 5*1024*1024;
                //大于5M，不允许上传
                if(fileSize>FIVE_M){
                    this.$message.error("最大上传5M")
                    return  false
                }
                //判断文件类型，必须是xlsx格式
                let fileName = file.name
                let reg = /^.+(\.pdf)$/
                if(!reg.test(fileName)){
                    this.$message.error("只能上传pdf!")
                    return false
                }
                return true
            },
            // 文件数量过多时提醒
            handleExceed() {
                this.$message({ type: 'error', message: '最多支持1个附件上传' })
            },
            query() {
                homeworkApi.getPageCount(this.queryForm.homeworkId, this.queryForm.homeworkTitle).then(res => {
                    this.pageCount = res;
                    this.pageIndex = 1;
                    this.getPage(1);
                });
            },
            getPage(pageIndex) {
                homeworkApi.getPage(pageIndex, this.queryForm.homeworkId, this.queryForm.homeworkTitle).then(res => {
                    this.tableData = res;
                });
            },
            editStudentHomework(homeworkId) {
                homeworkApi.getHomework(homeworkId).then(res => {
                    this.entityForm = res;
                    this.editing = true;
                })
            },
            save() {
                homeworkApi.submitHomework(this.entityForm).then(() => {
                    this.$message.success("成功");
                    this.getPage(this.pageIndex);
                    this.editing = false;
                });
            }
        },
        created() {
            this.query();
        }
    }
</script>

<style scoped>

</style>