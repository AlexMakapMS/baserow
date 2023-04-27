import { Registerable } from '@baserow/modules/core/registry'
import ParagraphElement from '@baserow/modules/builder/components/elements/components/ParagraphElement'
import HeadingElement from '@baserow/modules/builder/components/elements/components/HeadingElement'
import ParagraphElementForm from '@baserow/modules/builder/components/elements/components/forms/ParagraphElementForm'
import HeadingElementForm from '@baserow/modules/builder/components/elements/components/forms/HeadingElementForm'
import ImageElement from '@baserow/modules/builder/components/elements/components/ImageElement'
import ImageElementForm from '@baserow/modules/builder/components/elements/components/forms/ImageElementForm'

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

export class ImageElementType extends ElementType {
  getType() {
    return 'image'
  }

  get name() {
    return this.app.i18n.t('elementType.image')
  }

  get description() {
    return this.app.i18n.t('elementType.imageDescription')
  }

  get iconClass() {
    return 'image'
  }

  get component() {
    return ImageElement
  }

  get formComponent() {
    return ImageElementForm
  }

  getComponentProps(element) {
    return {
      element,
    }
  }
}
