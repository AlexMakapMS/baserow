import { Registerable } from '@baserow/modules/core/registry'

export class DeviceType extends Registerable {
  get iconClass() {
    return null
  }

  get order() {
    return null
  }

  get minWidth() {
    return 0
  }

  get maxWidth() {
    return 0
  }
}

export class DesktopDeviceType extends DeviceType {
  getType() {
    return 'desktop'
  }

  get iconClass() {
    return 'desktop'
  }

  get order() {
    return 1
  }

  get minWidth() {
    return 1100
  }

  get maxWidth() {
    return null // Can be as wide as you want
  }
}

export class TabletDeviceType extends DeviceType {
  getType() {
    return 'tablet'
  }

  get iconClass() {
    return 'tablet'
  }

  get order() {
    return 2
  }

  get minWidth() {
    return 768
  }

  get maxWidth() {
    return 768
  }
}

export class SmartphoneDeviceType extends DeviceType {
  getType() {
    return 'smartphone'
  }

  get iconClass() {
    return 'mobile'
  }

  get order() {
    return 3
  }

  get minWidth() {
    return 420
  }

  get maxWidth() {
    return 420
  }
}
