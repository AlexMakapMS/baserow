import { Registerable } from '@baserow/modules/core/registry'
import ParagraphElement from '@baserow/modules/builder/components/elements/components/ParagraphElement'
import HeadingElement from '@baserow/modules/builder/components/elements/components/HeadingElement'
import LinkElement from '@baserow/modules/builder/components/elements/components/LinkElement'
import LinkElementEdit from '@baserow/modules/builder/components/elements/components/LinkElementEdit'
import ParagraphElementForm from '@baserow/modules/builder/components/elements/components/forms/ParagraphElementForm'
import HeadingElementForm from '@baserow/modules/builder/components/elements/components/forms/HeadingElementForm'
import LinkElementForm from '@baserow/modules/builder/components/elements/components/forms/LinkElementForm'

import { compile } from 'path-to-regexp'

export class ElementType extends Registerable {
  get name() {
    return null
  }

  get description() {
    return null
  }

  get iconClass() {
    return null
  }

  get component() {
    return null
  }

  get editComponent() {
    return this.component
  }

  get formComponent() {
    return null
  }
}

export class HeadingElementType extends ElementType {
  getType() {
    return 'heading'
  }

  get name() {
    return this.app.i18n.t('elementType.heading')
  }

  get description() {
    return this.app.i18n.t('elementType.headingDescription')
  }

  get iconClass() {
    return 'heading'
  }

  get component() {
    return HeadingElement
  }

  get formComponent() {
    return HeadingElementForm
  }
}

export class ParagraphElementType extends ElementType {
  getType() {
    return 'paragraph'
  }

  get name() {
    return this.app.i18n.t('elementType.paragraph')
  }

  get description() {
    return this.app.i18n.t('elementType.paragraphDescription')
  }

  get iconClass() {
    return 'paragraph'
  }

  get component() {
    return ParagraphElement
  }

  get formComponent() {
    return ParagraphElementForm
  }
}

export class LinkElementType extends ElementType {
  getType() {
    return 'link'
  }

  get name() {
    return this.app.i18n.t('elementType.link')
  }

  get description() {
    return this.app.i18n.t('elementType.linkDescription')
  }

  get iconClass() {
    return 'link'
  }

  get component() {
    return LinkElement
  }

  get editComponent() {
    return LinkElementEdit
  }

  get formComponent() {
    return LinkElementForm
  }

  static getUrlFromElement(element, builder) {
    if (element.navigation_type === 'page') {
      if (!isNaN(element.navigate_to_page_id)) {
        const page = builder.pages.find(
          ({ id }) => id === element.navigate_to_page_id
        )

        // The builder page list might be empty or the page has been deleted
        if (!page) {
          return ''
        }

        const toPath = compile(page.path, { encode: encodeURIComponent })
        const pageParams = Object.fromEntries(
          element.page_parameters.map(({ name, value }) => [name, value])
        )
        return toPath(pageParams)
      }
    } else {
      return element.navigate_to_url
    }
    return ''
  }
}
