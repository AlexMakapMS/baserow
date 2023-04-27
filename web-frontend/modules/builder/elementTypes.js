import { Registerable } from '@baserow/modules/core/registry'
import ParagraphElement from '@baserow/modules/builder/components/elements/components/ParagraphElement'
import HeadingElement from '@baserow/modules/builder/components/elements/components/HeadingElement'
import LinkElement from '@baserow/modules/builder/components/elements/components/LinkElement'
import LinkElementEdit from '@baserow/modules/builder/components/elements/components/LinkElementEdit'
import ParagraphElementForm from '@baserow/modules/builder/components/elements/components/forms/ParagraphElementForm'
import HeadingElementForm from '@baserow/modules/builder/components/elements/components/forms/HeadingElementForm'
import LinkElementForm from '@baserow/modules/builder/components/elements/components/forms/LinkElementForm'

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

  get properties() {
    return []
  }

  /**
   * Extracts the attributes of the element instance into attributes that the component
   * can use. The returned object needs to be a mapping from the name of the property
   * at the component level to the value in the element object.
   *
   * Example:
   * - Let's say you have a prop called `level`
   * - The element looks like this: { 'id': 'someId', 'level': 1 }
   *
   * Then you will have to return { 'level': element.level }
   *
   * @param element
   * @returns {{}}
   */
  getComponentProps(element) {
    return {}
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

  getComponentProps(element) {
    return {
      value: element.value,
      level: element.level,
    }
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

  getComponentProps(element) {
    return {
      value: element.value,
    }
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

  getComponentProps(element) {
    return {
      value: element.value,
      alignment: element.alignment,
      variant: element.variant,
      width: element.width,
      target: element.target,
      navigation_type: element.navigation_type,
      navigate_to_page_id: element.navigate_to_page_id,
      navigate_to_url: element.navigate_to_url,
      page_parameters: element.page_parameters,
    }
  }
}
