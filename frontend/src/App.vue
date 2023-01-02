<script setup>
import { ref, onMounted, computed } from 'vue'
import { formatDistance } from 'date-fns'
import Device from './components/Device.vue'

const applicationName = ref(import.meta.env.VITE_APPLICATION_NAME || 'tasmota.fflnvb.de')
document.title = applicationName.value

const firstLoad= ref(true)
const isLoading= ref(true)
const devices = ref([])
const lastUpdate = ref('')
const searchQuery = ref('')
const searchColumn = ref('name')
const sortColumn = ref('name')
const sortReverse = ref(false)
const distance = ref('No update')

onMounted(() => {
    updateDevices()
    setInterval(updateDistance, 1000)
})

const filteredDevices = computed(() => {
    
    return devices.value
    .filter((device) => {
        if (searchColumn.value == 'name') {
            return device.Status.DeviceName.toLowerCase().includes(searchQuery.value.toLowerCase())
        } else if (searchColumn.value == 'topic') {
                return device.Status.Topic.toLowerCase().includes(searchQuery.value.toLowerCase())
            }
        })
        .sort(function(a, b){
            let first
            let second
            if (sortColumn.value == 'name') {
                first = a.Status.DeviceName
                second = b.Status.DeviceName
            } else if (sortColumn.value == 'topic') {
                first = a.Status.Topic
                second = b.Status.Topic
            } else if (sortColumn.value == 'signal') {
                first = b.StatusSTS.Wifi.Signal
                second = a.StatusSTS.Wifi.Signal
            } else if (sortColumn.value == 'version') {
                first = a.StatusFWR.Version
                second = b.StatusFWR.Version
            }
            if(sortReverse.value) {
                return first < second
            } else {
                return first > second
            }
        })
})

const filterClass = computed(() => {
    let out = []
    let columns = ['name', 'topic', 'signal', 'version']
    columns.forEach((column) => {
        if(sortColumn.value != column) {
            out[column] = "bi-arrow-down-up text-muted"
        } else if (sortReverse.value) {
            out[column] = "bi-arrow-up"
        } else {
            out[column] = "bi-arrow-down"
        }
    })
    return out
})

const updateDistance = () => {
    if (lastUpdate.value == '') {
        distance.value= 'No update'
    } else {
        let calcDistance = formatDistance(
            new Date(lastUpdate.value),
            new Date(),
            { includeSeconds: true }
        )
        distance.value = 'Last update: ' + calcDistance + ' ago'
    }
}

const changeSort = (column) => {
    if (sortColumn.value == column) {
        sortReverse.value = !sortReverse.value
    } else {
        sortReverse.value = false
    }
    sortColumn.value = column
}

const updateDevices = () => {
    isLoading.value = true
    const socket = new WebSocket('ws://' + location.hostname + ':8081')
    socket.addEventListener('open', (event) => {
        socket.send('getDevices')
    })
    socket.addEventListener('message', function (event) {
        let data = JSON.parse(event.data)
        devices.value = data.devices
        lastUpdate.value = data.created
        firstLoad.value = false
        isLoading.value = false
    })
}

</script>

<template>
    <div class="container" id="deviceList">
        <h1 class="display-5 mt-3">{{ applicationName }}</h1>
        <div class="float-end my-3">
            <i>{{ distance }}</i>
            <button v-on:click="updateDevices()"  :disabled="isLoading" class="btn btn-sm btn-secondary ms-2 refresh">
                <img :class="{ loading: isLoading }" src="@/assets/svg/arrow-clockwise.svg"/>
            </button>
        </div>
        <div id="deviceSearch" class="input-group w-100 mb-4">
            <select class="form-select" v-model="searchColumn">
                <option value="name">Name</option>
                <option value="topic">Topic</option>
            </select>
            <input type="text" class="form-control" v-model="searchQuery"
                placeholder="Search" aria-label="Namenssuche">
            <button type="button" class="btn btn-light clearSearch" v-if="searchQuery" v-on:click="searchQuery = ''">
                <i class="bi bi-x-lg"></i>
            </button>
        </div>
        <div>
            <ul class="list-group mb-5">
                <li class="list-group-item">
                    <div class="row fw-bold">
                        <div class="col-6">
                            Name
                            <i role="button" class="ms-1 bi" v-on:click="changeSort('name')" :class="filterClass['name']"></i>
                        </div>
                        <div class="col-2">
                            Topic
                            <i role="button" class="ms-1 bi" v-on:click="changeSort('topic')" :class="filterClass['topic']"></i>
                        </div>
                        <div class="col-2">
                            Signal
                            <i role="button" class="ms-1 bi" v-on:click="changeSort('signal')" :class="filterClass['signal']"></i>
                        </div>
                        <div class="col-2">
                            Version
                            <i role="button" class="ms-1 bi" v-on:click="changeSort('version')" :class="filterClass['version']"></i>
                        </div>
                    </div>
                </li>
                <li v-for="device of filteredDevices" :key="device.Status.DeviceName" class="list-group-item">
                    <Device :device="device"/>
                </li>
                <li v-if="firstLoad" class="list-group-item text-center py-3">
                    <div class="spinner-border text-secondary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </li>
            </ul>
        </div>

        
    </div>
    
    
</template>

<style scoped>
    button:focus, 
    input:focus {
        outline: none !important;
        box-shadow: none;
    }
    #deviceList {
        max-width: 800px;
    }
    #deviceSearch select {
        max-width: 150px;
    }
    .refresh {
        line-height: 16px;
    }
    .loading {
        animation: spin 1s linear 0s infinite;
        display: inline-block;
    }

    @keyframes spin {
        from {
            transform:rotate(0deg);
        }
        to {
            transform:rotate(360deg);
        }
    }
</style>
