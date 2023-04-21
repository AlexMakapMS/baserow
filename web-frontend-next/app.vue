<template>
  <div>
    <Logo />
    <Badge primary>Primary</Badge>

    <div style="width: 250px">
      <Dropdown
        :value="value"
        :disabled="disabled"
        @change="handleDropdownChange($event)"
      >
        <DropdownItem
          ref="dropdownItem1"
          name="Unicode (UTF-8)"
          value="utf-8"
        ></DropdownItem>
        <DropdownItem
          ref="dropdownItem2"
          name="Chinese, Simplified (GBK)"
          value="gbk"
        ></DropdownItem>
        <DropdownItem
          ref="dropdownItem3"
          name="Chinese (GB18030)"
          value="gb18030"
        ></DropdownItem>
        <DropdownItem
          ref="dropdownItem4"
          name="Chinese Traditional (Big5)"
          value="big5"
        ></DropdownItem>
        <DropdownItem
          ref="dropdownItem5"
          name="Cyrillic (KOI8-R)"
          value="koi8-r"
        ></DropdownItem>
        <DropdownItem
          ref="dropdownItem6"
          name="Cyrillic (KOI8-U)"
          value="koi8-u"
        ></DropdownItem>
      </Dropdown>
    </div>
  </div>
</template>

<script>
export default {
  // Please keep in sync with
  // src/baserow/contrib/database/api/export/serializers.py:SUPPORTED_EXPORT_CHARSETS
  name: "CharsetDropdown",
  props: {
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      value: null,
    };
  },
  methods: {
    handleDropdownChange(value) {
      this.value = value;
    },
  },
};
</script>
