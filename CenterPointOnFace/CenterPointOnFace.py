import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # Let user select a planar face
        face_selection = ui.selectEntity("Select a planar face", "PlanarFaces")
        selected_face = adsk.fusion.BRepFace.cast(face_selection.entity)

        if not selected_face:
            ui.messageBox("No valid face selected.")
            return

        # Get bounding box center
        face_box = selected_face.boundingBox
        center = face_box.minPoint.copy()
        center.translateBy(adsk.core.Vector3D.create(
            (face_box.maxPoint.x - face_box.minPoint.x) / 2,
            (face_box.maxPoint.y - face_box.minPoint.y) / 2,
            (face_box.maxPoint.z - face_box.minPoint.z) / 2
        ))

        # Create a sketch on the face
        sketches = rootComp.sketches
        sketch = sketches.add(selected_face)

        # Convert center to sketch space and add a point
        sketchCenter = sketch.modelToSketchSpace(center)
        sketchPoints = sketch.sketchPoints
        sketchPoints.add(sketchCenter)

        ui.messageBox("Center point added!")

    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
