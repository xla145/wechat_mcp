<template>
  <div class="article-edit">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑文章' : '新建文章' }}</span>
          <el-button @click="goBack">返回</el-button>
        </div>
      </template>

      <el-form 
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="article-form"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>

        <el-form-item label="作者" prop="author">
          <el-input v-model="form.author" placeholder="请输入作者" />
        </el-form-item>

        <el-form-item label="缩略图" prop="thumbnail_url">
          <el-upload
            class="thumbnail-uploader"
            :action="uploadUrl"
            :show-file-list="false"
            :on-success="handleThumbnailSuccess"
            :before-upload="beforeThumbnailUpload"
          >
            <img v-if="form.thumbnail_url_show" :src="form.thumbnail_url_show" class="thumbnail" />
            <el-icon v-else class="thumbnail-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="摘要" prop="digest">
          <el-input
            v-model="form.digest"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要"
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="10"
            placeholder="请输入文章内容"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="goBack">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

export default {
  name: 'ArticleEdit',
  components: {
    Plus
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const formRef = ref(null)
    const isEdit = ref(false)
    const uploadUrl = 'http://localhost:8000/api/v1/articles/upload_thumbnail'

    const form = ref({
      title: '',
      author: '',
      thumbnail_url: '',
      thumbnail_url_show: '',
      digest: '',
      content: ''
    })

    const rules = {
      title: [
        { required: true, message: '请输入文章标题', trigger: 'blur' },
        { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
      ],
      author: [
        { required: true, message: '请输入作者', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入文章内容', trigger: 'blur' },
        { min: 10, message: '内容不能少于10个字符', trigger: 'blur' }
      ]
    }

    const fetchArticle = async (id) => {
      try {
        const response = await axios.get(`/articles/${id}`)
        form.value = response.data
      } catch (error) {
        ElMessage.error('获取文章失败')
      }
    }

    const submitForm = async () => {
      if (!formRef.value) return
      
      try {
        await formRef.value.validate()
        
        if (isEdit.value) {
          await axios.put(`/articles/${route.params.id}`, form.value)
          ElMessage.success('更新成功')
        } else {
          await axios.post('/articles', form.value)
          ElMessage.success('创建成功')
        }
        
        router.push('/')
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }

    const handleThumbnailSuccess = (response) => {
      form.value.thumbnail_url = response.data.media_id
      form.value.thumbnail_url_show = response.data.url
    }

    const beforeThumbnailUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }
      return true
    }

    const goBack = () => {
      router.push('/')
    }

    onMounted(() => {
      const id = route.params.id
      if (id) {
        isEdit.value = true
        fetchArticle(id)
      }
    })

    return {
      formRef,
      form,
      rules,
      isEdit,
      uploadUrl,
      submitForm,
      handleThumbnailSuccess,
      beforeThumbnailUpload,
      goBack
    }
  }
}
</script>

<style scoped>
.article-edit {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.article-form {
  max-width: 800px;
  margin: 0 auto;
}
.thumbnail-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 178px;
  height: 178px;
}
.thumbnail-uploader:hover {
  border-color: #409EFF;
}
.thumbnail-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
  line-height: 178px;
}
.thumbnail {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}
</style> 