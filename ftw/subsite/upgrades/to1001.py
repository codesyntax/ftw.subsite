from ftw.upgrade import UpgradeStep
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility


class FixAttributes(UpgradeStep):

    MANAGER_NAMES = set("ftw.subsite.front{0}".format(index)
                        for index in range(1, 8))

    def __call__(self):
        self.migrate_portlet_assignments(self.portal)
        for obj in self.objects(
                {'object_provides':
                    'plone.app.layout.navigation.interfaces.INavigationRoot'},
                'Migrate teaser portlet assignments'):
            self.migrate_portlet_assignments(obj)

    def migrate_portlet_assignments(self, obj):
        try:
            annotations = IAnnotations(obj)
        except TypeError:
            # The obj has no annotations
            return

        known_manager = annotations.get(
            'plone.portlets.contextassignments', [])

        for managername in tuple(known_manager):
            if not managername in self.MANAGER_NAMES:
                continue

            manager = getUtility(IPortletManager, name=managername,
                                 context=obj)
            assignments = getMultiAdapter((obj, manager),
                                          IPortletAssignmentMapping,
                                          context=obj)
            for assignment in assignments.values():
                assignment.image = assignment.__dict__.pop('image', None)
